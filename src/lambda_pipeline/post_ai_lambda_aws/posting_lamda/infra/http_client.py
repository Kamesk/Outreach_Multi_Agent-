import requests

class HTTPClient:

    @staticmethod
    def post(url, headers=None, json=None):
        return requests.post(url, headers=headers, json=json)

    @staticmethod
    def put(url, headers=None, data=None):
        return requests.put(url, headers=headers, data=data)

    @staticmethod
    def get(url):
        return requests.get(url)
