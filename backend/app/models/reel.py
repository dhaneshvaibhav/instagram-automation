from pydantic import BaseModel
from typing import Optional

class ReelData(BaseModel):
    reel_id: str
    message: str
    keyword: Optional[str] = None

class ReelUpdate(BaseModel):
    message: str
    keyword: Optional[str] = None
