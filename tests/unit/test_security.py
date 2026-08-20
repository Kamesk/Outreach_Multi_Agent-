import hashlib
import hmac
import time
import pytest
from fastapi import HTTPException
from src.utils.security import validate_service_url, verify_hmac

def test_valid_webhook_signature(monkeypatch):
    monkeypatch.setattr("src.utils.security.settings.webhook_signing_secret", "test-secret")
    body = b'{"text":"hello"}'
    timestamp = str(int(time.time()))
    signature = hmac.new(b"test-secret", f"{timestamp}.".encode() + body, hashlib.sha256).hexdigest()
    verify_hmac(timestamp, signature, body)

def test_rejects_untrusted_service_url(monkeypatch):
    monkeypatch.setattr("src.utils.security.settings.allowed_service_url_hosts", ("smba.trafficmanager.net",))
    with pytest.raises(HTTPException):
        validate_service_url("https://evil.example/collector")
