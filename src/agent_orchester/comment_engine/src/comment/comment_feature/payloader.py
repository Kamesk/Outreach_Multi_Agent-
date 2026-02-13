from dotenv import load_dotenv
from src.comment.llm.response_generator import generate_llm_response
from src.comment.comment_feature.replier import post_reply_to_linkedin
from src.comment.components import get_dynamodb_table
from boto3.dynamodb.conditions import Key, Attr
from src.comment.utils.logger import get_logger

import os

logger = get_logger("payloader")
load_dotenv()
table = get_dynamodb_table()

def process_comment_payload(post_id, post_text):
    try:
        response = table.query(
            IndexName="SK-index", #GSI
            KeyConditionExpression=Key("SK").eq(post_id),
            FilterExpression=Attr("llm_response").not_exists() | 
                             Attr("llm_response").eq(None) | 
                             Attr("llm_response").eq("")
        )

        items = response.get("Items", [])
        if not items:
            logger.info(f"No unprocessed comments for post ID: {post_id}")
            return

        comment = sorted(items, key=lambda x: x["timestamp"], reverse=True)[0]

        comment_id = comment["PK"]
        comment_text = comment["comment_text"]
        activity_id = comment["activity_id"]

        logger.info(f"Generating LLM reply for comment ID: {comment_id}")
        llm_reply = generate_llm_response(comment_text, post_text)

        if not llm_reply:
            logger.warning("LLM failed to generate a response.")
            return

        success = post_reply_to_linkedin(activity_id, comment_id, llm_reply)

        if success:
            table.update_item(
                Key={"PK": comment_id, "SK": post_id},
                UpdateExpression="SET llm_response = :r, replied_to_linkedin = :t",
                ExpressionAttributeValues={
                    ":r": llm_reply,
                    ":t": True
                }
            )
            logger.info(f"Posted and updated DB for comment: {comment_id}")
        else:
            logger.warning(f"Failed to post reply for comment ID: {comment_id}")

    except Exception as e:
        logger.error(f"Error processing comment payload: {e}")
