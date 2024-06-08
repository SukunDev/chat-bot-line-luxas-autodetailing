from .line import Line
from typing import Optional
from .exceptions import ParamsError

class ReplyMessage(Line):
    def __init__(self, reply_token: Optional[str] = None, text: Optional[str] = None):
        super().__init__()
        if not reply_token:
            raise ParamsError("params 'reply_token' not found")
        if not text:
            raise ParamsError("params 'text' not found")
        self._send_message(reply_token=reply_token, text=text)
    