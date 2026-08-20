import urllib.parse
from config import settings
from src.utils.http import request

def refresh_access_token():
    r=request("POST", "https://www.linkedin.com/oauth/v2/accessToken",data={"grant_type":"refresh_token","refresh_token":settings.refresh_token,"client_id":settings.client_id,"client_secret":settings.client_secret})
    return r.json().get("access_token") if r.status_code==200 else None

def headers(params=None):
    h=(params or {}).get("headers",{}).copy();
    if "Authorization" in h: h["Authorization"]=h["Authorization"].replace("${ACCESS_TOKEN}",settings.access_token or "")
    if "X-API-KEY" in h: h["X-API-KEY"]=h["X-API-KEY"].replace("${X_API_KEY}",settings.x_api_key or "")
    return h

def get_latest_post(params_yaml):
    if not settings.access_token or not settings.org_id: return None
    org=f"urn:li:organization:{settings.org_id}"; p=(params_yaml.get("params",{}) or {}).copy(); p["author"]=org
    r=request("GET", "https://api.linkedin.com/rest/posts",headers=headers(params_yaml),params=p)
    if r.status_code==401:
        token=refresh_access_token()
        if not token:return None
        h=headers(params_yaml);h["Authorization"]=f"Bearer {token}";r=request("GET", "https://api.linkedin.com/rest/posts",headers=h,params=p)
    if r.status_code!=200:return None
    el=r.json().get("elements",[])
    if not el:return None
    return {"post_urn":el[0].get("id"),"post_text":el[0].get("commentary","") ,"headers":headers(params_yaml)}

def fetch_comments(post_urn,h):
    url=f"https://api.linkedin.com/rest/socialActions/{urllib.parse.quote(post_urn,safe='')}/comments";r=request("GET", url,headers=h)
    return r.json().get("elements",[]) if r.status_code==200 else []

def post_comment_reply(activity_id,comment_id,text):
    clean=lambda x:x.split(":")[-1] if x.startswith("urn:") else x
    url=f"{settings.unipile_base_url}/api/v1/posts/{clean(activity_id)}/comments"
    payload={"account_id":settings.ac_id,"text":text,"as_organization":settings.org_id,"comment_id":clean(comment_id)}
    r=request("POST", url,headers={"X-API-KEY":settings.x_api_key,"Content-Type":"application/json"},json=payload)
    return r.status_code in (200,201)
