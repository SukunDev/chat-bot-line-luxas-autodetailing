from .line import Line
from typing import Optional
from . import exceptions
import json

class MessageHandler(Line):
    def __init__(self):
        super().__init__()
        self._on_message_handler = None
        self._on_post_back_handler = None

    def handler(self, signature: Optional[str] = None, body: Optional[str] = None):
        if not signature:
            raise exceptions.ParamsError("parameter 'signature' not found")
        if not body:
            raise exceptions.ParamsError("parameter 'body' not found")
        self._validate_signature(signature=signature, body=body)
        if self._on_message_handler:
            event = json.loads(body)['events'][0]
            if event['type'] == "message":
                self._on_message_handler(event)
            if event['type'] == "postback":
                self._on_post_back_handler(event)
        else:
            raise Exception("No message handler registered")

    def onMessage(self, func):
        def wrapper(event):
            func(event)

        self._on_message_handler = wrapper
        return wrapper
    
    def onPostBack(self, func):
        def wrapper(event):
            func(event)

        self._on_post_back_handler = wrapper
        return wrapper