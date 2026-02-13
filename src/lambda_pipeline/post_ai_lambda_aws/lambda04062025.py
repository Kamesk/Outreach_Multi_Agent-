import os
import json
import boto3
import requests

s3 = boto3.client('s3')


def upload_image_to_linkedin(image_url, access_token, org_id):
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
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

    r = requests.post(register_url, headers=headers, json=body)
    if r.status_code != 200:
        raise Exception(f"Failed to register upload: {r.text}")
    
    upload_info = r.json()
    upload_url = upload_info["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    asset_urn = upload_info["value"]["asset"]
    img_data = requests.get(image_url).content
    upload_resp = requests.put(upload_url, data=img_data, headers={"Authorization": f"Bearer {access_token}"})
    
    if upload_resp.status_code not in [201, 200]:
        raise Exception(f"Image upload failed: {upload_resp.status_code} - {upload_resp.text}")
    
    return asset_urn


def post_to_linkedin(content, asset_urn, access_token, org_id):
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

    response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=body)
    print(f"LinkedIn response: {response.status_code} - {response.text}")



def lambda_handler(event, context):
    bucket = "falaiposting"
    prefix = "approved/"
    access_token = os.getenv("ACCESS_TOKEN")
    org_id = os.getenv("ORG_ID_TARGET")

    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' not in response or len(response['Contents']) == 0:
            print("No approved posts found.")
            return {"statusCode": 200, "body": "No approved post to process."}

        key = response['Contents'][0]['Key']
        print(f"Processing file: {key}")

        obj = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(obj["Body"].read().decode("utf-8"))

        content = data.get("text", "")
        image_url = data.get("image_url", "")

        print(f"Post preview: {content[:100]}")

        asset_urn = upload_image_to_linkedin(image_url, access_token, org_id)
        post_to_linkedin(content, asset_urn, access_token, org_id)
        s3.delete_object(Bucket=bucket, Key=key)

        return {"statusCode": 200, "body": f"Posted content from {key}"}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": str(e)}

