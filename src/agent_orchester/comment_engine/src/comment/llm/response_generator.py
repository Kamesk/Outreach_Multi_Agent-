import openai
import time
from src.comment.config.config import settings, prompts, params
from src.comment.utils.logger import get_logger

logger = get_logger("llm")

openai.api_key = settings.OPENAI_API_KEY


def generate_llm_response(comment_text, post_text, retries=3, delay=2):
    for attempt in range(retries):
        try:
            system_prompt = prompts["reply_to_comment"]["system"]
            user_prompt = prompts["reply_to_comment"]["user"].format(
                comment=comment_text,
                post_summary=post_text
            )

            response = openai.ChatCompletion.create(
                model=params["openai"]["model"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=params["openai"]["temperature"],
                max_tokens=params["openai"]["max_tokens"],
                top_p=params["openai"]["top_p"],
                frequency_penalty=params["openai"]["frequency_penalty"],
                presence_penalty=params["openai"]["presence_penalty"]
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            logger.warning(f"LLM attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    logger.error("All retries failed.")
    return None
