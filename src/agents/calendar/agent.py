import json
from datetime import datetime,timedelta
from config import settings
from src.clients.microsoft.auth import get_access_token
from src.clients.microsoft.graph import get_availability,create_event
from src.services.calendar.availability import extract_busy_ranges,generate_available_slots
from src.services.calendar.notification import notify
from src.utils.guardrails import validate_confirmation_payload,GuardrailError
from src.utils.time_utils import get_time_range
from src.utils.response import success,failure

def run(event):
    try:
        if "confirmed_slot" in event:
            start,end,email=validate_confirmation_payload(event); token=get_access_token()
            created=create_event(token,event.get("subject","Meeting"),start,end,[email]); notify("New Meeting Scheduled",f"Meeting with {email} at {start}")
            return success({"message":"Meeting scheduled","event":created})
        if event.get("sender_id") or event.get("message"):
            token=get_access_token(); now,start,end=get_time_range(); data=get_availability(token,start,end)
            schedule=data["value"][0]; busy=extract_busy_ranges(schedule.get("scheduleItems",[])); slots=generate_available_slots(now,start,schedule.get("availabilityView",[]),busy)
            return success({"available_slots":slots})
        return success({"message":"Ignored event"})
    except GuardrailError as exc: return failure(exc,400)
    except Exception as exc: return failure(exc)
