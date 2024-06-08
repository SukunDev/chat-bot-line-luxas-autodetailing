import base64
import hashlib
import hmac
import requests

def create_signature(secret, body) -> str:
    hash = hmac.new(secret.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash).decode('utf-8')
    return signature

def req(url, json = None, headers = None):
    base_headers = {}
    if headers:
        base_headers.update(headers)
    if not json:
        response = requests.get(url, headers=base_headers)
        return response
    response = requests.post(url, json=json, headers=base_headers)
    return response