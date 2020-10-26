from fastapi import APIRouter, Depends, Response, HTTPException
from app.models import User, Post, PostTag, UserTag, Tag
from app.database import get_db
from app.auth import get_current_user
from app.schemas.user import PostResponse
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get('/feed', response_model=List[PostResponse])
async def feed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user feed
    :param current_user: Current authentificated user
    :param db: Session instance
    :return: Posts related to tags user subscribed
    """
    feeds = db.query(Post)\
        .join(PostTag, PostTag.post_id == Post.id)\
        .join(UserTag, UserTag.tag_id == PostTag.tag_id)\
        .filter(
            UserTag.user_id == current_user.id
        )

    return [PostResponse.from_orm(f) for f in feeds]
