import re
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Request
from src.orchestrator.agent import run
from src.shared.teams import send_message
from src.utils.security import validate_service_url, verified_json
from src.clients.aws.s3 import read_json, upload_json
router=APIRouter()

@router.post('/teams/webhook')
async def teams_webhook(request: Request):
    body=await verified_json(request); message=body.get('text','')
    if not message:return {'status':'ignored'}
    response=run(message,body); text=response.get('body',response) if isinstance(response,dict) else str(response)
    if body.get('serviceUrl') and body.get('conversation',{}).get('id'):
        send_message(validate_service_url(body['serviceUrl']),body['conversation']['id'],str(text))
    return {'status':'sent','response':text}

@router.get('/health')
def health():return {'status':'alive'}

@router.post('/drafts/{draft_id}/approve')
async def approve_draft(draft_id: str, request: Request):
    """Protected internal approval operation; never expose this URL publicly."""
    if not re.fullmatch(r"[0-9a-f-]{36}", draft_id):
        raise HTTPException(status_code=400, detail="Invalid draft id")
    payload = await verified_json(request)
    approver = str(payload.get("approved_by", "")).strip()
    if not approver or len(approver) > 128:
        raise HTTPException(status_code=400, detail="approved_by is required")
    key = f"drafts/{draft_id}.json"
    try:
        draft = read_json(key)
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Draft not found") from exc
    if draft.get("status") != "PENDING_APPROVAL":
        raise HTTPException(status_code=409, detail="Draft is not awaiting approval")
    draft.update(status="APPROVED", approved_by=approver, approved_at=datetime.now(timezone.utc).isoformat())
    upload_json(f"approved/{draft_id}.json", draft)
    upload_json(key, draft)
    return {"id": draft_id, "status": "APPROVED"}
