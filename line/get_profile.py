from .line import Line
from typing import Optional
from .exceptions import ParamsError

class GetProfile(Line):
    def __init__(self, user_id: Optional[str] = None):
        if not user_id:
            raise ParamsError("params 'user_id' not found")
        
        self.__response = self._get_profile(user_id=user_id)
        self._userId = user_id
        self._displayName = None
        self._language = None
    
    @property
    def displayName(self):
        if self._displayName:
            return self._displayName
        self._displayName = self.__response['displayName']
        return self._displayName
    
    @property
    def language(self):
        if self._language:
            return self._language
        self._language = self.__response['language']
        return self._language
    
    @property
    def userId(self):
        if self._userId:
            return self._userId
        self._userId = self.__response['userId']
        return self._userId