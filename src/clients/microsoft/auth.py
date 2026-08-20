from msal import ConfidentialClientApplication
from config import settings

def get_access_token():
    app=ConfidentialClientApplication(settings.client_id, authority=f"https://login.microsoftonline.com/{settings.tenant_id}", client_credential=settings.client_secret)
    result=app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result: raise RuntimeError(f"Token acquisition failed: {result.get('error_description')}")
    return result["access_token"]
