import json
import boto3
from config import Settings

class S3Service:

    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_REGION
        )

    def upload_metadata(self, key: str, data: dict):
        self.client.put_object(
            Bucket=Settings.BUCKET_NAME,
            Key=key,
            Body=json.dumps(data),
            ContentType="application/json"
        )