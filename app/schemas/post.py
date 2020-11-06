from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .tag import TagModel


class PostCreateUpdateModel(BaseModel):
    id: Optional[int] = None
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
    updated_at: datetime

    class Config:
        orm_mode = True
