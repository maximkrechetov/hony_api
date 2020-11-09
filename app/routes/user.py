from fastapi import APIRouter, Depends, Response, HTTPException
from app.models import User, Post, PostTag, UserTag, Tag
from app.database import get_db
from app.auth import get_current_user
from app.schemas.post import PostRetrieveModel, AuthorModel
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get('/feed', response_model=List[PostRetrieveModel])
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
    posts = db.query(Post)\
        .join(PostTag, PostTag.post_id == Post.id)\
        .join(UserTag, UserTag.tag_id == PostTag.tag_id)\
        .filter(
            UserTag.user_id == current_user.id
        ).all()

    tags = db.query(
        PostTag.tag_id,
        PostTag.post_id,
        Tag.title
    )\
        .join(Tag, PostTag.tag_id == Tag.id)\
        .filter(PostTag.post_id.in_([p.id for p in posts])).all()

    result = []

    for post in posts:
        result.append({
            'id': post.id,
            'title': post.title,
            'preview_text': post.preview_text,
            'text': post.text,
            'cover': post.cover,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'author': AuthorModel(first_name=post.author.first_name,
                                  last_name=post.author.last_name),
            'tags': [{'id': t[0], 'title': t[2]}
                     for t in list(filter(lambda x: x.post_id == post.id, tags))]
        })

    return result
