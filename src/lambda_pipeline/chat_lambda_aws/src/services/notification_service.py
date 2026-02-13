import boto3
from config import SNS_TOPIC_ARN
from utils.logger import get_logger

logger = get_logger("sns")
sns = boto3.client("sns")


def notify(subject, event_time, email):
    if not SNS_TOPIC_ARN:
        return

    message = (
        f"Meeting scheduled with {email}\n"
        f"Time: {event_time.strftime('%A %d %B %Y %H:%M')}"
    )

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )