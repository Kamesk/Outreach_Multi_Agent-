from infra.http_client import HTTPClient
from utils.logger import get_logger

logger = get_logger("linkedin_post")

POST_URL = "https://api.linkedin.com/v2/ugcPosts"


class LinkedInPostService:

    @staticmethod
    def create_post(content, asset_urn, access_token, org_id):

        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": "202403",
            "Content-Type": "application/json"
        }

        body = {
            "author": f"urn:li:organization:{org_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {"text": "Auto-posted content"},
                            "media": asset_urn,
                            "title": {"text": "Auto Image Post"}
                        }
                    ]
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        response = HTTPClient.post(POST_URL, headers=headers, json=body)

        if response.status_code not in [200, 201]:
            raise Exception(f"LinkedIn post failed: {response.text}")

        return response.json()
