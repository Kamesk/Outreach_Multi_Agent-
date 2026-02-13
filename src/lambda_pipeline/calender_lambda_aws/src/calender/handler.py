import json
from datetime import datetime, timedelta
from utils.time_utils import get_time_range
from utils.response import success, error
from services.auth_service import get_access_token
from services.graph_calendar_service import create_event
from services.availability_service import get_availability
from services.notification_service import notify


def lambda_handler(event, context):
    try:
        print("Incoming event:", json.dumps(event))

        if "confirmed_slot" in event:
            return _handle_confirmation(event)

        if "sender_id" in event:
            return _handle_availability()

        return success({"message": "Ignored event"})

    except Exception as e:
        return error(str(e))


def _handle_availability():
    access_token = get_access_token()
    now, start, end = get_time_range()

    availability = get_availability(access_token, start, end)

    return success({"availability": availability})


def _handle_confirmation(event):
    access_token = get_access_token()

    start_time = datetime.fromisoformat(event["confirmed_slot"])
    end_time = start_time + timedelta(minutes=30)

    attendee = event["email"]

    event_data = create_event(
        access_token,
        event.get("subject", "Meeting"),
        start_time,
        end_time,
        [attendee]
    )

    notify(
        "New Meeting Scheduled",
        f"Meeting with {attendee} at {start_time}"
    )

    return success({"event": event_data})
