import json
import boto3
from shared.intent import classify_intent
from shared.teams import send_to_teams
from shared.state import BaseAgentState

lambda_client = boto3.client("lambda")


CHAT_LAMBDA_NAME = "chat_lambda"
CALENDAR_LAMBDA_NAME = "calendar_lambda"

def invoke_lambda(function_name: str, payload: dict) -> dict:
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload)
    )

    result = json.loads(response["Payload"].read())
    return result

def lambda_handler(event, context):

    try:
        user_message = event.get("text")
        user_id = event.get("user_id")
        channel_id = event.get("channel_id")

        if not user_message:
            return {"statusCode": 400, "body": "Missing message"}

        intent = classify_intent(user_message)
        if intent == "calendar":

            calendar_response = invoke_lambda(
                CALENDAR_LAMBDA_NAME,
                {
                    "user_id": user_id,
                    "message": user_message
                }
            )

            final_response = calendar_response.get("body")

        else:
            chat_response = invoke_lambda(
                CHAT_LAMBDA_NAME,
                {
                    "user_id": user_id,
                    "message": user_message
                }
            )

            final_response = chat_response.get("body")

        send_to_teams(channel_id, final_response)

        return {
            "statusCode": 200,
            "body": "Processed successfully"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
