from datetime import datetime, timedelta
from config import UK_TZ

def get_time_range():
    now = datetime.now(UK_TZ)
    start = now.replace(hour=9, minute=0, second=0, microsecond=0)
    end = (now + timedelta(days=30)).replace(hour=18, minute=0, second=0, microsecond=0)
    return now, start, end
