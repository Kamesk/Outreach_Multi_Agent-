from src.clients.llm.openai import generate_text
from src.clients.llm.fal import generate_image

def generate(system,user,image_prompt): return generate_text(system,user),generate_image(image_prompt)
