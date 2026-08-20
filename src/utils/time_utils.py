from datetime import datetime, timedelta
from config import settings

def get_time_range():
    now = datetime.now(settings.uk_tz)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=settings.max_forward_days)
    return now, start, end
