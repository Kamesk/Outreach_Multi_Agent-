import json
from infra.aws_client import get_s3_client
from utils.logger import get_logger

logger = get_logger("s3")

class S3Service:

    def __init__(self):
        self.client = get_s3_client()

    def get_next_object(self, bucket, prefix):
        response = self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)

        if "Contents" not in response or not response["Contents"]:
            return None

        return response["Contents"][0]["Key"]

    def read_json(self, bucket, key):
        obj = self.client.get_object(Bucket=bucket, Key=key)
        return json.loads(obj["Body"].read().decode("utf-8"))

    def delete(self, bucket, key):
        self.client.delete_object(Bucket=bucket, Key=key)
