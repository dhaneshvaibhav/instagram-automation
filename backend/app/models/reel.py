from pydantic import BaseModel
from typing import Optional, List, Union

class Button(BaseModel):
    type: str # 'web_url' or 'postback'
    title: str
    url: Optional[str] = None
    payload: Optional[str] = None

class ReelData(BaseModel):
    reel_id: str
    message: str
    keyword: Optional[str] = None
    all_users: Optional[bool] = True
    buttons: Optional[Union[str, List[Button]]] = None

class ReelUpdate(BaseModel):
    message: str
    keyword: Optional[str] = None
    all_users: Optional[bool] = True
    buttons: Optional[Union[str, List[Button]]] = None
