import requests
from msal import ConfidentialClientApplication
from config import settings

def get_bot_access_token():
    authority=f"https://login.microsoftonline.com/{settings.tenant_id}"
    app=ConfidentialClientApplication(settings.client_id, authority=authority, client_credential=settings.client_secret)
    result=app.acquire_token_for_client(scopes=["https://api.botframework.com/.default"])
    if "access_token" not in result: raise RuntimeError(f"Failed to acquire Teams token: {result}")
    return result["access_token"]

def send_message(service_url, conversation_id, text):
    token=get_bot_access_token(); url=f"{service_url}/v3/conversations/{conversation_id}/activities"
    r=requests.post(url, headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"}, json={"type":"message","text":text})
    if r.status_code not in (200,201): raise RuntimeError(f"Teams message failed: {r.status_code} - {r.text}")
    return r.json()

# Backward-compatible alias for old callers.
send_to_teams = send_message
