from langchain_openai import ChatOpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set")

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


VALID_INTENTS = ["chat", "calendar", "posting", "ingestion"]


def classify_intent(message: str) -> str:

    prompt = f"""
    Classify the user request into exactly one of:
    chat, calendar, posting, ingestion.

    Only return the label.

    User message:
    {message}
    """

    response = _llm.invoke(prompt).content.strip().lower()

    for intent in VALID_INTENTS:
        if intent in response:
            return intent

    return "chat"
