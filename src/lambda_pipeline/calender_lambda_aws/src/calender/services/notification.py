import boto3
from config import SNS_TOPIC_ARN

sns = boto3.client("sns")

def notify(subject, message):
    if not SNS_TOPIC_ARN:
        return

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )