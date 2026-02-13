import os
import requests
from msal import ConfidentialClientApplication


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

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
        raise RuntimeError(f"Failed to acquire Teams token: {result}")

    return result["access_token"]


def send_message(service_url: str, conversation_id: str, text: str):

    token = get_bot_access_token()

    url = f"{service_url}/v3/conversations/{conversation_id}/activities"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "type": "message",
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code not in [200, 201]:
        raise RuntimeError(
            f"Teams message failed: {response.status_code} - {response.text}"
        )

    return response.json()
