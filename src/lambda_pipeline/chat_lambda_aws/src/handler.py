import json
from utils.response import success, failure
from utils.time_utils import get_time_range
from guardrails import validate_confirmation_payload, GuardrailError
from services.auth_service import get_access_token
from services.graph_service import create_event, get_availability
from services.notification_service import notify
from core.slot_engine import extract_busy_ranges, generate_available_slots


def lambda_handler(event, context):
    try:
        if "confirmed_slot" in event:
            return handle_confirmation(event)

        if "sender_id" in event and "sender_name" in event:
            return handle_availability()

        return success({"message": "Ignored event"})

    except Exception as e:
        return failure(str(e))


def handle_availability():
    access_token = get_access_token()
    now, start, end = get_time_range()

    availability = get_availability(access_token, start, end)

    schedule = availability["value"][0]
    busy_ranges = extract_busy_ranges(schedule["scheduleItems"])

    slots = generate_available_slots(
        now,
        start,
        schedule["availabilityView"],
        busy_ranges
    )

    return success({"available_slots": slots})


def handle_confirmation(event):
    try:
        start_time, end_time, email = validate_confirmation_payload(event)
        access_token = get_access_token()

        event_data = create_event(
            access_token,
            event.get("subject", "Meeting"),
            start_time,
            end_time,
            [email]
        )

        notify("New Meeting Scheduled", start_time, email)

        return success({"message": "Meeting scheduled", "event": event_data})

    except GuardrailError as g:
        return failure(f"Validation error: {str(g)}")
