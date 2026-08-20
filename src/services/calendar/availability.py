from datetime import datetime, timedelta
from config import settings

def extract_busy_ranges(schedule_items):
    def parse(value):
        value = value.get("dateTime") if isinstance(value, dict) else value
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(settings.uk_tz)
    return [(parse(item["start"]), parse(item["end"])) for item in schedule_items if item.get("status") not in ("free", "0")]

def generate_available_slots(now,start,availability_view,busy_ranges):
    slots=[]; end_limit=start+timedelta(days=settings.max_forward_days)
    for i,status in enumerate(availability_view):
        if len(slots)>=settings.max_return_slots: break
        slot_start=start+timedelta(minutes=settings.slot_interval_minutes*i); slot_end=slot_start+timedelta(minutes=settings.slot_interval_minutes)
        if slot_end<=now or slot_start>end_limit or slot_start.weekday()>=5: continue
        if not (settings.business_start<=slot_start.hour<settings.business_end) or status!="0": continue
        if any(b[0]<slot_end and b[1]>slot_start for b in busy_ranges): continue
        slots.append(slot_start.isoformat())
    return slots
