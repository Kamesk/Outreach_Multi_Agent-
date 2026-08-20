import boto3,os

def get_table():
    return boto3.resource("dynamodb",region_name=os.getenv("AWS_REGION","eu-west-2")).Table(os.getenv("DYNAMODB_TABLE_NAME","Commentpayloads"))
