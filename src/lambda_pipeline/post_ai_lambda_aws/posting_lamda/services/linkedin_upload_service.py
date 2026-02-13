from infra.http_client import HTTPClient
from utils.logger import get_logger

logger = get_logger("linkedin_upload")

REGISTER_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"


class LinkedInUploadService:

    @staticmethod
    def upload_image(image_url, access_token, org_id):

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        body = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": f"urn:li:organization:{org_id}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }

        response = HTTPClient.post(REGISTER_URL, headers=headers, json=body)

        if response.status_code != 200:
            raise Exception(f"Register upload failed: {response.text}")

        data = response.json()
        upload_url = data["value"]["uploadMechanism"][
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
        ]["uploadUrl"]

        asset_urn = data["value"]["asset"]

        image_bytes = HTTPClient.get(image_url).content

        upload_resp = HTTPClient.put(
            upload_url,
            headers={"Authorization": f"Bearer {access_token}"},
            data=image_bytes
        )

        if upload_resp.status_code not in [200, 201]:
            raise Exception(f"Image upload failed: {upload_resp.text}")

        return asset_urn
