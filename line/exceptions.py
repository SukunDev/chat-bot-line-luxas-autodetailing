class LineError(Exception):
    """Line Error"""

class ParamsError(LineError):
    """Params Error"""

class SignatureError(LineError):
    """Signature Error"""

class ReplyMessageError(LineError):
    """Reply Message Error"""