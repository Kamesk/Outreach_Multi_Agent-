from msal import ConfidentialClientApplication
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID

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
        raise RuntimeError(
            f"Token error: {token_response.get('error_description')}"
        )

    return token_response["access_token"]