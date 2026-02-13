import os
from zoneinfo import ZoneInfo

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
USER_EMAIL = os.getenv("USER_EMAIL")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

UK_TZ = ZoneInfo("Europe/London")
BUSINESS_START = 9
BUSINESS_END = 17
MAX_FORWARD_DAYS = 30
SLOT_INTERVAL_MINUTES = 30
MAX_RETURN_SLOTS = 30
