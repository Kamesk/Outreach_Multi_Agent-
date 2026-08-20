"""Authentication and request-origin controls for public endpoints."""
import hashlib
import hmac
import time
from urllib.parse import urlparse
from fastapi import HTTPException, Request
from config import settings

MAX_AGE_SECONDS = 300

def verify_hmac(timestamp: str | None, signature: str | None, body: bytes) -> None:
    if not settings.webhook_signing_secret:
        raise HTTPException(status_code=503, detail="Webhook authentication is not configured")
    try:
        ts = int(timestamp or "")
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid webhook timestamp") from exc
    if abs(time.time() - ts) > MAX_AGE_SECONDS:
        raise HTTPException(status_code=401, detail="Expired webhook request")
    expected = hmac.new(settings.webhook_signing_secret.encode(), f"{ts}.".encode() + body, hashlib.sha256).hexdigest()
    if not signature or not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

async def verified_json(request: Request) -> dict:
    body = await request.body()
    if len(body) > 64 * 1024:
        raise HTTPException(status_code=413, detail="Request body is too large")
    verify_hmac(request.headers.get("X-Outreach-Timestamp"), request.headers.get("X-Outreach-Signature"), body)
    try:
        payload = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="JSON body must be an object")
    return payload

def validate_service_url(value: str) -> str:
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host or not any(host == allowed or host.endswith("." + allowed) for allowed in settings.allowed_service_url_hosts):
        raise HTTPException(status_code=400, detail="Untrusted service URL")
    return value
