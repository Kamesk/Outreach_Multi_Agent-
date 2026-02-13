import openai
from config import Settings

openai.api_key = Settings.OPENAI_API_KEY

class OpenAIClient:

    @staticmethod
    def generate_text(system_prompt: str, user_prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
