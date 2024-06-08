from .line import Line
from typing import Optional
from .exceptions import ParamsError

class ReplyFlexMessage(Line):
    def __init__(self, user_id: Optional[str] = None, text: Optional[str] = None, data: Optional[str] = None):
        super().__init__()
        if not user_id:
            raise ParamsError("params 'user_id' not found")
        if not data:
            raise ParamsError("params 'data' not found")
        if not text:
            raise ParamsError("params 'text' not found")
        self._send_flex_message(user_id=user_id, text=text, data=data)
    