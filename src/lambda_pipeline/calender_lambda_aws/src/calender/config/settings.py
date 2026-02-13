import os
from zoneinfo import ZoneInfo

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
USER_EMAIL = os.getenv("USER_EMAIL")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

UK_TZ = ZoneInfo("Europe/London")