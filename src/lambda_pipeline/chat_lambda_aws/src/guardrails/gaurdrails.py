import re
from datetime import datetime, timedelta
from config import (
    UK_TZ, BUSINESS_START, BUSINESS_END,
    MAX_FORWARD_DAYS, SLOT_INTERVAL_MINUTES
)

class GuardrailError(Exception):
    pass


def validate_email(email: str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not email or not re.match(pattern, email):
        raise GuardrailError("Invalid email format.")


def validate_iso_datetime(dt_str: str) -> datetime:
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.astimezone(UK_TZ)
    except Exception:
        raise GuardrailError("Invalid ISO datetime format.")


def validate_booking_window(dt: datetime):
    now = datetime.now(UK_TZ)

    if dt <= now:
        raise GuardrailError("Cannot book past time.")

    if dt > now + timedelta(days=MAX_FORWARD_DAYS):
        raise GuardrailError("Booking exceeds allowed window.")


def validate_business_hours(dt: datetime):
    if dt.weekday() >= 5:
        raise GuardrailError("Weekend booking not allowed.")

    if not (BUSINESS_START <= dt.hour < BUSINESS_END):
        raise GuardrailError("Outside business hours.")


def validate_slot(start: datetime, end: datetime):
    if (end - start).total_seconds() != SLOT_INTERVAL_MINUTES * 60:
        raise GuardrailError("Invalid slot duration.")


def validate_confirmation_payload(payload):
    confirmed_slot = payload.get("confirmed_slot")
    email = payload.get("email")

    if not confirmed_slot:
        raise GuardrailError("Missing confirmed_slot.")

    if not email:
        raise GuardrailError("Missing email.")

    validate_email(email)
    start_time = validate_iso_datetime(confirmed_slot)
    end_time = start_time + timedelta(minutes=SLOT_INTERVAL_MINUTES)

    validate_booking_window(start_time)
    validate_business_hours(start_time)
    validate_slot(start_time, end_time)

    return start_time, end_time, email
