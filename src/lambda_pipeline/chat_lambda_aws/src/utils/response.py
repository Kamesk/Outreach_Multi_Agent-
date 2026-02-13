import json

def success(body):
    return {"statusCode": 200, "body": json.dumps(body)}

def failure(message):
    return {"statusCode": 500, "body": json.dumps({"error": str(message)})}