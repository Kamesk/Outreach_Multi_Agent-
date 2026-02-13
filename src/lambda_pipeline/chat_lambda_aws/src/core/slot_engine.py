from datetime import datetime, timedelta
from config import (
    UK_TZ, BUSINESS_START, BUSINESS_END,
    MAX_RETURN_SLOTS, SLOT_INTERVAL_MINUTES
)


def extract_busy_ranges(schedule_items):
    return [
        (
            datetime.fromisoformat(item["start"]["dateTime"]).astimezone(UK_TZ),
            datetime.fromisoformat(item["end"]["dateTime"]).astimezone(UK_TZ)
        )
        for item in schedule_items
    ]


def generate_available_slots(now, start, availability_view, busy_ranges):
    slots = []
    end_limit = (now + timedelta(days=3)).replace(
        hour=23, minute=59, second=59, microsecond=999999
    )

    for i, status in enumerate(availability_view):
        if len(slots) >= MAX_RETURN_SLOTS:
            break

        slot_start = start + timedelta(minutes=SLOT_INTERVAL_MINUTES * i)
        slot_end = slot_start + timedelta(minutes=SLOT_INTERVAL_MINUTES)

        if slot_end <= now:
            continue
        if slot_start > end_limit:
            continue
        if slot_start.weekday() >= 5:
            continue
        if not (BUSINESS_START <= slot_start.hour < BUSINESS_END):
            continue
        if status != "0":
            continue
        if any(b[0] < slot_end and b[1] > slot_start for b in busy_ranges):
            continue

        slots.append(slot_start.isoformat())

    return slots
