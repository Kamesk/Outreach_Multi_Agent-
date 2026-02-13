from msal import ConfidentialClientApplication
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID
from utils.logger import get_logger

logger = get_logger("auth")

def get_access_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"

    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )

    token_response = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    if "access_token" not in token_response:
        logger.error(token_response)
        raise RuntimeError("Token acquisition failed.")

    return token_response["access_token"]
