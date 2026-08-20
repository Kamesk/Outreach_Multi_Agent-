"""A small explicit approval gate for outward-facing content.

Production callers must invoke this from a protected internal approval UI or
workflow.  Generated content is never publishable merely because it exists.
"""
import json
import uuid
from datetime import datetime, timezone
from src.clients.aws.s3 import upload_json, read_json

def create_draft(text: str, images: dict) -> dict:
    draft_id = str(uuid.uuid4())
    draft = {
        "id": draft_id,
        "status": "PENDING_APPROVAL",
        "text": text,
        "images": images,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "approved_by": None,
        "published_at": None,
    }
    upload_json(f"drafts/{draft_id}.json", draft)
    return draft

def approved_payload(key: str) -> dict:
    data = read_json(key)
    if data.get("status") != "APPROVED" or not data.get("approved_by"):
        raise PermissionError("Only explicitly approved drafts may be published")
    if data.get("published_at"):
        raise RuntimeError("Draft was already published")
    return data
