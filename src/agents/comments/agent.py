from src.services.comments.fetcher import get_latest_post_and_comments
from src.services.comments.processor import process_comment_payload

def run(event=None):
    post, comments = get_latest_post_and_comments()
    if not post:
        return {"message": "No post found"}
    # The existing DynamoDB processor selects the newest unprocessed comment for the post.
    # Execute once to avoid repeatedly selecting the same record.
    response = process_comment_payload(post["post_urn"], post["post_text"])
    return {"post_urn": post["post_urn"], "comments_found": len(comments), "response": response}
