import yaml
from pathlib import Path
from src.clients.llm.openai import generate_text
from config import settings

def generate_reply(comment_text,post_text):
    # Treat third-party content as data, not instructions.
    comment_text = (comment_text or "")[:settings.max_comment_chars]
    post_text = (post_text or "")[:settings.max_post_chars]
    p=yaml.safe_load((Path(__file__).resolve().parents[2]/"prompts"/"comments.yaml").read_text())["reply_to_comment"]
    return generate_text(p["system"],p["user"].format(comment=comment_text,post_summary=post_text),temperature=0.2,max_tokens=150)
