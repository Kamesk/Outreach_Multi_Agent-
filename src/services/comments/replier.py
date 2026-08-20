from src.clients.linkedin.client import post_comment_reply

def reply(activity_id,comment_id,text): return post_comment_reply(activity_id,comment_id,text)
