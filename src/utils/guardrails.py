import re
from datetime import datetime, timedelta
from config import settings

class GuardrailError(Exception): pass

def validate_email(email: str):
    if not email or not re.match(r"^[\w.\-]+@[\w.\-]+\.\w+$", email):
        raise GuardrailError("Invalid email format.")

def validate_iso_datetime(value: str) -> datetime:
    try: return datetime.fromisoformat(value).astimezone(settings.uk_tz)
    except Exception as exc: raise GuardrailError("Invalid ISO datetime format.") from exc

def validate_booking_window(dt):
    now=datetime.now(settings.uk_tz)
    if dt <= now: raise GuardrailError("Cannot book past time.")
    if dt > now + timedelta(days=settings.max_forward_days): raise GuardrailError("Booking exceeds allowed window.")

def validate_business_hours(dt):
    if dt.weekday() >= 5 or not (settings.business_start <= dt.hour < settings.business_end):
        raise GuardrailError("Outside business hours.")

def validate_confirmation_payload(payload):
    slot=payload.get("confirmed_slot"); email=payload.get("email")
    if not slot: raise GuardrailError("Missing confirmed_slot.")
    if not email: raise GuardrailError("Missing email.")
    validate_email(email); start=validate_iso_datetime(slot); end=start+timedelta(minutes=settings.slot_interval_minutes)
    validate_booking_window(start); validate_business_hours(start)
    return start,end,email
