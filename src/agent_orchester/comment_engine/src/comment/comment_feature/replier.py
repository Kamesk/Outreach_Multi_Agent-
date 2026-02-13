import requests
from src.comment.config.config import settings, get_unipile_headers
from src.comment.utils.logger import get_logger

logger = get_logger("replier")

def strip_urn_prefix(urn):
    return urn.split(":")[-1] if urn.startswith("urn:") else urn

def post_reply_to_linkedin(activity_id, comment_id, reply_text):
    clean_activity_id = strip_urn_prefix(activity_id)
    clean_comment_id = strip_urn_prefix(comment_id)
    print(f"Cleaned activity ID: {clean_activity_id}, Cleaned comment ID: {clean_comment_id}")

    url = f"{settings.UNIPILE_BASE_URL}/api/v1/posts/{clean_activity_id}/comments"

    payload = {
        "account_id": settings.AC_ID,
        "text": reply_text,
        "as_organization": settings.ORG_ID,
        "comment_id": clean_comment_id
    }
    print(f"Payload: {payload}")

    headers = get_unipile_headers()
    print("Final headers being sent:")
    print(headers)

    logger.info(f"Posting reply to Unipile: {url}")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        logger.info(f"Replied to comment ID: {clean_comment_id}")
        return True
    else:
        logger.error(f"Failed to post reply: {response.status_code} - {response.text}")
        return False
