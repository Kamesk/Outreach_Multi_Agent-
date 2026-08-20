import yaml
from pathlib import Path
from src.clients.linkedin.client import get_latest_post,fetch_comments

def load_params():
    return yaml.safe_load((Path(__file__).resolve().parents[2]/"prompts"/"comment_params.yaml").read_text())

def get_latest_post_and_comments():
    data=get_latest_post(load_params())
    if not data:return None,[]
    return data,fetch_comments(data["post_urn"],data["headers"])
