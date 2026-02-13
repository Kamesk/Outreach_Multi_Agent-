import boto3
from src.comment.config.config import settings
import os

dynamo_table_name = os.getenv("DYNAMODB_TABLE_NAME", "Commentpayloads")
dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
table = dynamodb.Table(dynamo_table_name)


def get_dynamodb_table():
    return table
