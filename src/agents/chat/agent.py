from config import settings
from src.shared.intent import classify_intent

def run(event):
    message=event.get('message') or event.get('text','')
    if not message:return {'statusCode':400,'body':'Missing message'}
    return {'statusCode':200,'body':f'General response: {message}'}
