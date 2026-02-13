import os
import json
import logging
import requests
from fastapi import FastAPI, Request
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from msal import ConfidentialClientApplication
from calendar_module import handle_calendar_request, handle_event_confirmation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("teams-agent")
app = FastAPI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://api.botframework.com/.default"]

def get_bot_access_token():
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" not in result:
        raise RuntimeError(f"Bot token error: {result}")

    return result["access_token"]

def calendar_tool(input_text: str):
    if "confirm" in input_text.lower():
        return handle_event_confirmation(json.loads(input_text))
    return handle_calendar_request({"message": input_text})

def chat_tool(input_text: str):
    return f"General response: {input_text}"


tools = [
    Tool(
        name="CalendarEngine",
        func=calendar_tool,
        description="Handles scheduling, availability and booking."
    ),
    Tool(
        name="ChatEngine",
        func=chat_tool,
        description="Handles general chat."
    ),
]


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)


@app.post("/teams/webhook")
async def teams_webhook(request: Request):

    body = await request.json()

    try:
        user_message = body.get("text", "")
        service_url = body.get("serviceUrl")
        conversation_id = body.get("conversation", {}).get("id")

        if not user_message:
            return {"status": "ignored"}

        # Run LangChain agent
        response_text = agent.run(user_message)

        # Send reply back to Teams
        access_token = get_bot_access_token()

        reply_url = f"{service_url}/v3/conversations/{conversation_id}/activities"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "type": "message",
            "text": response_text
        }

        r = requests.post(reply_url, headers=headers, json=payload)

        if r.status_code not in [200, 201]:
            logger.error(f"Teams reply failed: {r.text}")

        return {"status": "sent"}

    except Exception as e:
        logger.exception("Error handling Teams request")
        return {"error": str(e)}


@app.get("/health")
def health():
    return {"status": "alive"}
