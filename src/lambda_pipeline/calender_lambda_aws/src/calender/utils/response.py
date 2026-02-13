from datetime import datetime, timedelta
from config import UK_TZ
import json

def get_time_range():
    now = datetime.now(UK_TZ)
    start = now.replace(hour=9, minute=0, second=0, microsecond=0)
    end = (now + timedelta(days=30)).replace(hour=18, minute=0, second=0, microsecond=0)
    return now, start, end

def success(body):
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }

def error(message):
    return {
        "statusCode": 500,
        "body": json.dumps({"error": str(message)})
    }
