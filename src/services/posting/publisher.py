import requests
from config import settings

def upload_image(image_url):
    h={"Authorization":f"Bearer {settings.access_token}","Content-Type":"application/json","X-Restli-Protocol-Version":"2.0.0"}
    body={"registerUploadRequest":{"recipes":["urn:li:digitalmediaRecipe:feedshare-image"],"owner":f"urn:li:organization:{settings.org_id}","serviceRelationships":[{"relationshipType":"OWNER","identifier":"urn:li:userGeneratedContent"}]}}
    r=requests.post("https://api.linkedin.com/v2/assets?action=registerUpload",headers=h,json=body)
    if r.status_code!=200: raise RuntimeError(r.text)
    data=r.json()["value"]; mech=data["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]; asset=data["asset"]
    image=requests.get(image_url).content; up=requests.put(mech["uploadUrl"],headers={"Authorization":f"Bearer {settings.access_token}"},data=image)
    if up.status_code not in (200,201): raise RuntimeError(up.text)
    return asset

def publish(content,asset_urn):
    body={"author":f"urn:li:organization:{settings.org_id}","lifecycleState":"PUBLISHED","specificContent":{"com.linkedin.ugc.ShareContent":{"shareCommentary":{"text":content},"shareMediaCategory":"IMAGE","media":[{"status":"READY","description":{"text":"Auto-posted content"},"media":asset_urn,"title":{"text":"Auto Image Post"}}]}},"visibility":{"com.linkedin.ugc.MemberNetworkVisibility":"PUBLIC"}}
    h={"Authorization":f"Bearer {settings.access_token}","X-Restli-Protocol-Version":"2.0.0","LinkedIn-Version":"202403","Content-Type":"application/json"}
    r=requests.post("https://api.linkedin.com/v2/ugcPosts",headers=h,json=body)
    if r.status_code not in (200,201): raise RuntimeError(r.text)
    return r.json()
