from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .tag import TagModel


class AuthorModel(BaseModel):
    first_name: str
    last_name: str


class PostDeleteModel(BaseModel):
    post_id: int


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
    author: AuthorModel
    created_at: datetime
    updated_at: datetime
    tags: List[TagModel]

    class Config:
        orm_mode = True
