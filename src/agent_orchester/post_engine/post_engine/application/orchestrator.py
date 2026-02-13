import os
import requests
from datetime import datetime
from services.prompt_service import PromptService
from services.text_generation_service import TextGenerationService
from services.image_generation_service import ImageGenerationService
from services.s3_service import S3Service


class PostOrchestrator:

    def __init__(self):
        self.s3 = S3Service()

    def execute(self, prompt_path: str):
        system_prompt, user_prompt, image_prompt = PromptService.load_prompt(prompt_path)

        generated_text = TextGenerationService.generate(system_prompt, user_prompt)

        image_result = ImageGenerationService.generate(image_prompt)

        metadata = {}
        if image_result and "images" in image_result:
            for img in image_result["images"]:
                url = img["url"]
                metadata[url] = {
                    "generated_text": generated_text,
                    "timestamp": datetime.utcnow().isoformat()
                }

        self.s3.upload_metadata("temp/metadata.json", metadata)

        return {
            "text": generated_text,
            "images": metadata
        }
