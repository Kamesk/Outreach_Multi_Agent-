import requests
from config import USER_EMAIL

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

def create_event(access_token, subject, start_time, end_time, attendees):
    url = f"{GRAPH_BASE}/users/{USER_EMAIL}/events?sendUpdates=all"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "subject": subject,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Europe/London"
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Europe/London"
        },
        "location": {"displayName": "Online"},
        "attendees": [
            {
                "emailAddress": {
                    "address": email,
                    "name": email.split("@")[0].title()
                },
                "type": "required"
            }
            for email in attendees
        ],
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 201:
        raise RuntimeError(f"Event creation failed: {response.text}")

    return response.json()
