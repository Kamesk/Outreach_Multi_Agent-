from infra.openai_client import OpenAIClient

class TextGenerationService:

    @staticmethod
    def generate(system_prompt: str, user_prompt: str) -> str:
        return OpenAIClient.generate_text(system_prompt, user_prompt)
