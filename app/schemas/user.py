from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostResponse(BaseModel):
    id: int
    title: str
    text: str
    preview_text: Optional[str] = None
    cover: Optional[str] = None
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True

