import requests

ACCESS_TOKEN = "AQXFn2MZHdn2DJqbImviZAg_Nf78UjrrTdvCx_TiSGgdrn9XL8txYHtiTVh0DS0J5g5ZzLkhTmKbrdPymlldMPGroy1IyJkAbadPGraYE3KCm18ggEg8c5xFUzoNhKPsvWNp3jKwrQOJU_1ldIjBK5mNypANPnlqRtQgI4k3QERJPHMUVJ_lcmuH8H8BEPhm7H4kfgoqQ8L161ApPgPZEaDoW1hKqfS5qfZGAeLJzbtXIhzlL4-dFu3ctiWz5GlrcgWkwlr-fLqMKzpREyljLMJozhziTlhKjcyzEHIOL19ipIvL8xqA1pvbnqx6mNFNQcMVMIlpIhgCFclm0X4sDaTifl593g"
ORG_URN = "urn:li:organization:106444572"
LINKEDIN_API_URL = "https://api.linkedin.com/rest/posts"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "LinkedIn-Version": "202503"
}

params = {
    "q": "author",
    "author": ORG_URN,
    "count": 1,
    "start": 0
}

response = requests.get(LINKEDIN_API_URL, headers=headers, params=params)

if response.status_code == 200:
    print("Success")
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
