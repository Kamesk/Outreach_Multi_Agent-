from langchain_openai import ChatOpenAI
from config import settings

VALID_INTENTS=("chat","calendar","posting","ingestion","comments")

def classify_intent(message: str) -> str:
    if not settings.openai_api_key:
        return "chat"
    llm=ChatOpenAI(model="gpt-5.4-nano", temperature=0, api_key=settings.openai_api_key)
    prompt=f"Classify into exactly one of {', '.join(VALID_INTENTS)}. Return only the label.\nUser: {message}"
    result=llm.invoke(prompt).content.strip().lower()
    return next((x for x in VALID_INTENTS if x in result), "chat")
