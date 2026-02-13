import requests
from dotenv import load_dotenv
from src.comment.config.config import settings, get_linkedin_headers, get_params_yaml
from src.comment.utils.logger import get_logger
from src.comment.utils.linkedin_auth import refresh_access_token
import urllib.parse

logger = get_logger("fetcher")
load_dotenv()

def get_latest_post_id():
    ACCESS_TOKEN = settings.ACCESS_TOKEN
    ORG_ID = settings.ORG_ID
    

    if not ACCESS_TOKEN or not ORG_ID:
        logger.error("ACCESS_TOKEN or ORG_ID_TARGET missing in .env")
        return None

    ORG_URN = f"urn:li:organization:{ORG_ID}"
    logger.info(f"Fetching latest post for organization: {ORG_URN}")
    
    params_yaml = get_params_yaml()
    headers = get_linkedin_headers(params_yaml)
    params = params_yaml.get("params", {})
    params["author"] = ORG_URN

    url = "https://api.linkedin.com/rest/posts"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:
        logger.warning("Access token expired. Attempting to refresh...")
        new_token = refresh_access_token()
        if not new_token:
            logger.error("Token refresh failed.")
            return None
        headers["Authorization"] = f"Bearer {new_token}"
        response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        elements = response.json().get("elements", [])
        if not elements:
            logger.info("No posts found.")
            return None

        post = elements[0]
        post_urn = post.get("id")
        post_text = post.get("commentary", "")

        logger.info(f"Fetched post URN: {post_urn}")
        return {
            "post_urn": post_urn,
            "post_text": post_text,
            "headers": headers
        }
    else:
        logger.error(f"Failed to fetch posts: {response.status_code} - {response.text}")
        return None

def fetch_comments_by_post_id(post_urn, headers):
    encoded_urn = urllib.parse.quote(post_urn, safe='')
    url = f"https://api.linkedin.com/rest/socialActions/{encoded_urn}/comments"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Failed to fetch comments: {response.status_code} - {response.text}")
        return []

    comments = response.json().get("elements", [])
    logger.info(f"Fetched {len(comments)} comment(s).")
    return comments
