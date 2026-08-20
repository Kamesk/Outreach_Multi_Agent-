from src.shared.intent import classify_intent
from src.agents.chat.agent import run as chat
from src.agents.calendar.agent import run as calendar
from src.agents.posting.agent import run as posting
from src.agents.ingestion.agent import run as ingestion
from src.agents.comments.agent import run as comments

ROUTES={'chat':chat,'calendar':calendar,'posting':posting,'ingestion':ingestion,'comments':comments}

def run(message,event=None):
    payload=dict(event or {}); payload['message']=message
    intent=classify_intent(message)
    return ROUTES.get(intent,chat)(payload)
