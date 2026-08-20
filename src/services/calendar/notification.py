import boto3
from config import settings

def notify(subject, message):
    if not settings.sns_topic_arn: return None
    return boto3.client("sns", region_name=settings.aws_region).publish(TopicArn=settings.sns_topic_arn,Subject=subject,Message=message)
