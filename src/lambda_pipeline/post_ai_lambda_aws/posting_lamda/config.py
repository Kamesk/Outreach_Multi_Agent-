import os

class Settings:
    BUCKET_NAME = os.getenv("BUCKET_NAME", "falaiposting")
    PREFIX = os.getenv("PREFIX", "approved/")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ORG_ID = os.getenv("ORG_ID_TARGET")

    REQUIRED = ["ACCESS_TOKEN", "ORG_ID"]

    @classmethod
    def validate(cls):
        for var in cls.REQUIRED:
            if not getattr(cls, var):
                raise EnvironmentError(f"Missing environment variable: {var}")
