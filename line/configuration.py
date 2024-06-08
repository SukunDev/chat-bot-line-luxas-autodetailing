from .line import Line
from .exceptions import ParamsError
from typing import Optional


class Configuration(Line):
    def __init__(self, secret: Optional[str] = None, access_token: Optional[str] = None):
        super().__init__()
        if not secret:
            raise ParamsError("params 'secret' not found")
        if not access_token:
            raise ParamsError("params 'access_token' not found")
            
        Line.access_token = access_token
        Line.secret = secret


