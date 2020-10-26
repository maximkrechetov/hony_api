from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TagModel(BaseModel):
    id: Optional[int] = None
    title: str
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


class SubscribeModel(BaseModel):
    tag_id: int
