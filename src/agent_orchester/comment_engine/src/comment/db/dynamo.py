from datetime import datetime
from src.comment.utils.logger import get_logger
from src.comment.components import get_dynamodb_table

logger = get_logger("dynamodb")

def insert_comment(comment_id, comment_text, post_id, activity_id):
    table = get_dynamodb_table()
    try:
        response = table.get_item(Key={"PK": comment_id, "SK": post_id})
        if "Item" in response:
            logger.info(f"Comment already exists: {comment_id}")
            return

        item = {
            "PK": comment_id,
            "SK": post_id,
            "comment_id": comment_id,
            "comment_text": comment_text,
            "post_id": post_id,
            "activity_id": activity_id,
            "timestamp": datetime.utcnow().isoformat(),
            "llm_response": None,
            "replied_to_linkedin": False
        }
        logger.info(f"Inserting comment: {comment_text}")
        table.put_item(Item=item)
        logger.info(f"Inserted comment: {comment_id}")
    except Exception as e:
        logger.error(f"Error inserting comment: {e}")
