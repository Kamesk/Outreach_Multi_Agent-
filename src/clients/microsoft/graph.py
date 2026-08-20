import requests
from config import settings
GRAPH_BASE="https://graph.microsoft.com/v1.0"

def get_availability(access_token,start,end):
    url=f"{GRAPH_BASE}/users/{settings.user_email}/calendar/getSchedule"
    payload={"schedules":[settings.user_email],"startTime":{"dateTime":start.isoformat(),"timeZone":"GMT Standard Time"},"endTime":{"dateTime":end.isoformat(),"timeZone":"GMT Standard Time"},"availabilityViewInterval":30}
    r=requests.post(url,headers={"Authorization":f"Bearer {access_token}","Content-Type":"application/json"},json=payload)
    if r.status_code!=200: raise RuntimeError(f"Availability fetch failed: {r.text}")
    return r.json()

def create_event(access_token,subject,start,end,attendees):
    url=f"{GRAPH_BASE}/users/{settings.user_email}/events?sendUpdates=all"
    payload={"subject":subject,"start":{"dateTime":start.isoformat(),"timeZone":"Europe/London"},"end":{"dateTime":end.isoformat(),"timeZone":"Europe/London"},"location":{"displayName":"Online"},"attendees":[{"emailAddress":{"address":e,"name":e.split('@')[0].title()},"type":"required"} for e in attendees],"isOnlineMeeting":True,"onlineMeetingProvider":"teamsForBusiness"}
    r=requests.post(url,headers={"Authorization":f"Bearer {access_token}","Content-Type":"application/json"},json=payload)
    if r.status_code!=201: raise RuntimeError(f"Event creation failed: {r.text}")
    return r.json()
