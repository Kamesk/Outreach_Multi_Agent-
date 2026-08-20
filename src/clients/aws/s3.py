import boto3,json
from config import settings

def client(): return boto3.client("s3",region_name=settings.aws_region)

def upload_json(key,data): return client().put_object(Bucket=settings.bucket_name,Key=key,Body=json.dumps(data),ContentType="application/json")

def next_json():
    r=client().list_objects_v2(Bucket=settings.bucket_name,Prefix=settings.prefix)
    return r.get("Contents",[])[0]["Key"] if r.get("Contents") else None

def read_json(key): return json.loads(client().get_object(Bucket=settings.bucket_name,Key=key)["Body"].read().decode())

def delete(key): return client().delete_object(Bucket=settings.bucket_name,Key=key)
