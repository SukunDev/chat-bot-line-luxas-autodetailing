from typing import Optional
from . import  helper
from .exceptions import SignatureError, ReplyMessageError


class Line:
    """Line Module"""
    secret: str = None
    access_token: str = None
    base_url = "https://api.line.me/v2/bot"
    def _validate_signature(self, signature, body) -> None:
        created_signature = helper.create_signature(secret=Line.secret, body=body)
        if created_signature != signature:
            raise SignatureError("Failed to verify signature")
    
    def _send_message(self, reply_token, text):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Line.access_token}"
        }
        response = helper.req(f"{Line.base_url}/message/reply", json={
            "replyToken": reply_token,
            "messages":[
                {
                    "type": "text",
                    "text": text
                }
            ]
        }, headers=headers)
        if response.status_code != 200:
            raise ReplyMessageError("Failed while try reply message")
        return response.json()['sendMessages'][0]
    
    def _send_flex_message(self, user_id, text, data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Line.access_token}"
        }
        response = helper.req(f"{Line.base_url}/message/push", json={
            "to": user_id,
            "messages":[
                {
                    "type": "text",
                    "text": text
                },
                {
                    "type": "flex",
                    "altText": "This is a Flex Message",
                    "contents": data
                }
            ]
        }, headers=headers)
        if response.status_code != 200:
            raise ReplyMessageError("Failed while try reply message")
        return response.json()['sendMessages'][0]
    
    def _get_profile(self, user_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Line.access_token}"
        }
        response = helper.req(f"{Line.base_url}/profile/{user_id}", headers=headers)
        if response.status_code != 200:
            raise ReplyMessageError("Failed while try reply message")
        return response.json()