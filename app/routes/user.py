import sqlalchemy as sa
import shutil
import os

from fastapi import APIRouter, Depends, Response, HTTPException, Query, UploadFile, File
from app.models import User, Post, PostTag, UserTag, Tag
from app.database import get_db
from app.auth import get_current_user
from app.schemas.post import PostRetrieveModel, AuthorModel
from typing import List, Optional

router = APIRouter()


@router.get('/feed', response_model=List[PostRetrieveModel])
async def feed(
    limit: Optional[int] = Query(15),
    page: Optional[int] = Query(1),
    current_user: User = Depends(get_current_user),
    db: sa.orm.Session = Depends(get_db)
):
    """
    Get user feed
    :param limit: records on page limit
    :param page: page number
    :param current_user: Current authentificated user
    :param db: Session instance
    :return: Posts related to tags user subscribed
    """
    posts = db.query(Post)\
        .join(PostTag, PostTag.post_id == Post.id)\
        .join(UserTag, UserTag.tag_id == PostTag.tag_id)\
        .filter(
            UserTag.user_id == current_user.id
        ) \
        .order_by(sa.desc(PostTag.created_at)) \
        .limit(limit)\
        .offset(limit * (page - 1))

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


@router.post('/upload_avatar')
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: sa.orm.Session = Depends(get_db)
):
    """
    Uploads avatar and saves them
    :param file: File object
    :param current_user: Current authentificated user
    :param db: Session instance
    :return: Upload info
    """
    path = os.path.join('static/user_avatars', file.filename)

    with open(path, 'wb+') as buffer:
        shutil.copyfileobj(file.file, buffer)

    if current_user.avatar:
        if os.path.exists(current_user.avatar):
            os.remove(current_user.avatar)

    try:
        current_user.avatar = path
        db.add(current_user)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

    return {'filename': file.filename, 'path': path}
