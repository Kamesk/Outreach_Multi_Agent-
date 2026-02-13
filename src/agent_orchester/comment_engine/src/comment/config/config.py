import os
import yaml
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Core Environment Variables
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ORG_ID = os.getenv("ORG_ID_TARGET")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    AC_ID = os.getenv("AC_ID")
    UNIPILE_BASE_URL = "https://api13.unipile.com:14364"

    @staticmethod
    def _interpolate_env_vars(raw_content: str):
        # Replace placeholders with environment variables
        return (
            raw_content
            .replace("${ACCESS_TOKEN}", os.getenv("ACCESS_TOKEN", ""))
            .replace("${X_API_KEY}", os.getenv("X_API_KEY", ""))
            
        )

    @classmethod
    def load_yaml(cls, path: str):
        with open(path, "r") as f:
            raw = f.read()
            interpolated = cls._interpolate_env_vars(raw)
            return yaml.safe_load(interpolated)

    @classmethod
    def load_prompts(cls):
        return cls.load_yaml("prompts.yaml")

    @classmethod
    def load_params(cls):
        return cls.load_yaml("params.yaml")


def get_linkedin_headers(params_yaml=None):
    if params_yaml is None:
        params_yaml = Settings.load_params()
    headers = params_yaml.get("headers", {})
    if "Authorization" in headers and "${ACCESS_TOKEN}" in headers["Authorization"]:
        headers["Authorization"] = headers["Authorization"].replace("${ACCESS_TOKEN}", os.getenv("ACCESS_TOKEN", ""))
    return headers


def get_unipile_headers(params_yaml=None):
    if params_yaml is None:
        params_yaml = Settings.load_params()
    headers = params_yaml.get("headers", {})
    if "X-API-KEY" in headers and "${X_API_KEY}" in headers["X-API-KEY"]:
        headers["X-API-KEY"] = headers["X-API-KEY"].replace("${X_API_KEY}", os.getenv("X_API_KEY", ""))
    return headers


def get_params_yaml():
    return Settings.load_params()


# Optional module-level constants for convenience
settings = Settings()
prompts = settings.load_prompts()
params = settings.load_params()
