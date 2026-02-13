import requests
from datetime import timedelta, datetime
from config import USER_EMAIL, UK_TZ

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

def get_availability(access_token, start_time, end_time):
    url = f"{GRAPH_BASE}/users/{USER_EMAIL}/calendar/getSchedule"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "schedules": [USER_EMAIL],
        "startTime": {"dateTime": start_time.isoformat(), "timeZone": "GMT Standard Time"},
        "endTime": {"dateTime": end_time.isoformat(), "timeZone": "GMT Standard Time"},
        "availabilityViewInterval": 30
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Availability fetch failed: {response.text}")

    return response.json()