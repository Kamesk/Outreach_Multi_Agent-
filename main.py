import os
import sys
import json
from typing import TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from lambda_pipeline.chat_lambda.src.handler import lambda_handler as chat_handler
from lambda_pipeline.calender_lambda.src.calender.handler import lambda_handler as calendar_handler
from lambda_pipeline.post_ai_lambda.posting_lamda.handler import lambda_handler as posting_handler
from agent_orchester.Ingestion_engine.handler import lambda_handler as ingestion_handler

sys.path.append(os.path.abspath("src"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

def chat_tool(input_text: str):
    response = chat_handler(
        {"message": input_text},
        None
    )
    return response.get("body")


def calendar_tool(input_text: str):
    response = calendar_handler(
        {"message": input_text},
        None
    )
    return response.get("body")


def posting_tool(input_text: str):
    response = posting_handler(
        {},
        None
    )
    return response.get("body")


def ingestion_tool(input_text: str):
    response = ingestion_handler(
        {"source_folder": ".github/artifacts"},
        None
    )
    return response.get("body")


tools = [
    Tool(
        name="ChatEngine",
        func=chat_tool,
        description="Handles general AI chat and RAG queries."
    ),
    Tool(
        name="CalendarEngine",
        func=calendar_tool,
        description="Handles meeting scheduling, availability, and bookings."
    ),
    Tool(
        name="PostingEngine",
        func=posting_tool,
        description="Handles approved LinkedIn posting."
    ),
    Tool(
        name="IngestionEngine",
        func=ingestion_tool,
        description="Triggers document ingestion and RAG indexing."
    ),
]


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)


def main():
    print("\n=== Multi-Agent Controller ===\n")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        try:
            response = agent.run(user_input)
            print(f"\nAgent: {response}\n")

        except Exception as e:
            print(f"\nError: {e}\n")


def lambda_handler(event, context):
    """
    If you ever deploy this as a single orchestrator Lambda.
    """

    user_input = event.get("message")

    if not user_input:
        return {
            "statusCode": 400,
            "body": "Missing message"
        }

    response = agent.run(user_input)

    return {
        "statusCode": 200,
        "body": response
    }


if __name__ == "__main__":
    main()
