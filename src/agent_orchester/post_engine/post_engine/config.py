import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    FAL_KEY = os.getenv("FAL_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FINE_TUNE_ID = os.getenv("FINE_TUNE_ID")

    AWS_REGION = os.getenv("AWS_REGION")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    BUCKET_NAME = os.getenv("BUCKET_NAME", "falaiposting")

    REQUIRED = [
        "FAL_KEY",
        "OPENAI_API_KEY",
        "FINE_TUNE_ID",
        "AWS_REGION",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY"
    ]

    @classmethod
    def validate(cls):
        for var in cls.REQUIRED:
            if not getattr(cls, var):
                raise EnvironmentError(f"Missing environment variable: {var}")
