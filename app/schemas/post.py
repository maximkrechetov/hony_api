from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class PostCreateModel(BaseModel):
    text: str
    title: str
    preview_text: str
    cover: Optional[str] = None
    tags: Optional[List[int]] = []


class PostRetrieveModel(BaseModel):
    id: int
    title: str
    text: str
    preview_text: Optional[str] = None
    cover: Optional[str] = None
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True
