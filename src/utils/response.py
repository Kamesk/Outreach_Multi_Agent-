def success(body):
    return {"statusCode": 200, "body": body}

def failure(message, status_code=500):
    return {"statusCode": status_code, "body": str(message)}

def error(message, status_code=500):
    return failure(message, status_code)
