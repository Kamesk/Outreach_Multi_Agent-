from src.comment.config.config import settings, prompts, params
from src.comment.comment_feature.fetcher import fetch_comments_by_post_id, get_latest_post_id
from src.comment.comment_feature.payloader import process_comment_payload
from src.comment.utils.logger import get_logger
from src.comment.db.dynamo import insert_comment

logger = get_logger("main")

def main():
    logger.info("Fetching latest post...")
    post_info = get_latest_post_id()

    if not post_info:
        logger.error("Failed to fetch latest post.")
        return

    post_urn = post_info["post_urn"]
    post_text = post_info["post_text"]
    headers = post_info["headers"]

    logger.info(f"Fetched latest post: {post_urn}")

    comments = fetch_comments_by_post_id(post_urn, headers)
    if not comments:
        logger.info("No comments found on the latest post.")
        return

    for comment in comments:
        comment_id = comment.get("id")
        comment_text = comment.get("message", {}).get("text", "")
        activity_id = comment.get("object")

        logger.info(f"Inserting comment: {comment_text}")
        insert_comment(comment_id, comment_text, post_urn, activity_id)
        process_comment_payload(post_urn, post_text)

if __name__ == "__main__":
    main()
