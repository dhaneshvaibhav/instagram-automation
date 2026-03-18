from pydantic import BaseModel
from typing import Optional

class ReelData(BaseModel):
    reel_id: str
    mode: str = "dm"
    dm_message: Optional[str] = ""
    public_reply: Optional[str] = ""
    keyword: Optional[str] = None
    ai_enabled: bool = False
    ai_context: Optional[str] = None

class ReelUpdate(BaseModel):
    mode: str = "dm"
    dm_message: Optional[str] = ""
    public_reply: Optional[str] = ""
    keyword: Optional[str] = None
    ai_enabled: bool = False
    ai_context: Optional[str] = None
