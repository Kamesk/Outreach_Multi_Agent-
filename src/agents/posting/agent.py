from datetime import datetime,timezone
from src.services.posting.prompt import load
from src.services.posting.generation import generate
from src.clients.aws.s3 import upload_json,next_json,read_json,delete
from src.services.posting.publisher import upload_image,publish
from src.services.posting.approval import create_draft, approved_payload
from config import settings
from src.clients.aws.workflow import claim, finish

def generate_post(prompt_path):
    system,user,image_prompt=load(prompt_path); text,images=generate(system,user,image_prompt)
    if not text or len(text) > settings.max_post_chars:
        raise ValueError("Generated post is empty or exceeds the configured length")
    metadata={}
    for image in (images or {}).get("images",[]):
        url=image.get("url")
        if url: metadata[url]={"generated_text":text,"timestamp":datetime.now(timezone.utc).isoformat()}
    draft = create_draft(text, metadata)
    return {"message":"Draft created; human approval is required before publication.","draft_id":draft["id"],"status":draft["status"],"text":text,"images":metadata}

def publish_next():
    key=next_json()
    if not key:return {"message":"No approved post to process."}
    if not settings.allow_live_publish:
        return {"message":"Live publishing is disabled by configuration."}
    data=approved_payload(key)
    image_url = next(iter(data.get("images", {})), "")
    if not image_url:
        raise ValueError("Approved draft has no image asset")
    if not claim(data["id"]):
        return {"message":"Draft is already being processed or has already been sent."}
    try:
        asset=upload_image(image_url); result=publish(data["text"],asset)
        data["published_at"] = datetime.now(timezone.utc).isoformat()
        upload_json(key, data)
        finish(data["id"], "PUBLISHED")
        return {"message":f"Posted approved content from {key}","result":result}
    except Exception:
        finish(data["id"], "FAILED")
        raise

def run(event=None):
    if event and event.get("mode")=="publish": return publish_next()
    return generate_post((event or {}).get("prompt_path","src/prompts/post.yaml"))
