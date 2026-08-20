import fal_client
from config import settings

def generate_image(prompt):
    return fal_client.subscribe("fal-ai/flux-pro/v1.1-ultra-finetuned",arguments={"prompt":prompt,"guidance_scale":10,"seed":0,"sync_mode":False,"num_images":1,"enable_safety_checker":False,"aspect_ratio":"1:1","finetune_id":settings.fine_tune_id,"finetune_strength":0.7},with_logs=False)
