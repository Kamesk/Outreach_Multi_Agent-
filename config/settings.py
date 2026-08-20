import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    fal_key: str | None = os.getenv("FAL_KEY")
    fine_tune_id: str | None = os.getenv("FINE_TUNE_ID")
    aws_region: str = os.getenv("AWS_REGION", "eu-west-2")
    bucket_name: str = os.getenv("BUCKET_NAME", "falaiposting")
    prefix: str = os.getenv("PREFIX", "approved/")
    access_token: str | None = os.getenv("ACCESS_TOKEN")
    org_id: str | None = os.getenv("ORG_ID_TARGET")
    client_id: str | None = os.getenv("CLIENT_ID")
    client_secret: str | None = os.getenv("CLIENT_SECRET")
    tenant_id: str | None = os.getenv("TENANT_ID")
    user_email: str | None = os.getenv("USER_EMAIL")
    sns_topic_arn: str | None = os.getenv("SNS_TOPIC_ARN")
    ac_id: str | None = os.getenv("AC_ID")
    x_api_key: str | None = os.getenv("X_API_KEY")
    refresh_token: str | None = os.getenv("REFRESH_TOKEN")
    unipile_base_url: str = os.getenv("UNIPILE_BASE_URL", "https://api13.unipile.com:14364")
    business_start: int = int(os.getenv("BUSINESS_START", "9"))
    business_end: int = int(os.getenv("BUSINESS_END", "17"))
    max_forward_days: int = int(os.getenv("MAX_FORWARD_DAYS", "14"))
    slot_interval_minutes: int = int(os.getenv("SLOT_INTERVAL_MINUTES", "30"))
    max_return_slots: int = int(os.getenv("MAX_RETURN_SLOTS", "10"))
    uk_tz_name: str = "Europe/London"
    webhook_signing_secret: str | None = os.getenv("WEBHOOK_SIGNING_SECRET")
    allowed_service_url_hosts: tuple[str, ...] = tuple(
        host.strip().lower() for host in os.getenv(
            "ALLOWED_SERVICE_URL_HOSTS", "smba.trafficmanager.net"
        ).split(",") if host.strip()
    )
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "15"))
    max_post_chars: int = int(os.getenv("MAX_POST_CHARS", "3000"))
    max_comment_chars: int = int(os.getenv("MAX_COMMENT_CHARS", "500"))
    allow_live_publish: bool = os.getenv("ALLOW_LIVE_PUBLISH", "false").lower() == "true"
    workflow_table_name: str = os.getenv("WORKFLOW_TABLE_NAME", "OutreachWorkflows")

    @property
    def uk_tz(self):
        return ZoneInfo(self.uk_tz_name)

settings = Settings()
