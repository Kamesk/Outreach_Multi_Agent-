from infra.fal_client_wrapper import FalClient

class ImageGenerationService:

    @staticmethod
    def generate(prompt: str):
        return FalClient.generate_image(prompt)
