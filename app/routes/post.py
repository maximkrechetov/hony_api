from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from app.models import Post, User, Tag, PostTag
from app.database import get_db
from app.auth import get_current_user
from app.schemas.post import PostCreateModel


router = APIRouter()


@router.post('/create')
async def create(
    data: PostCreateModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Creates a new Post
    :param data: must be PostCreateModel comparable
    :param current_user: Current authenticated user
    :param db: Session instance
    :return: 201 Created
    """
    try:
        post = Post(
            text=data.text,
            cover=data.cover,
            author_id=current_user.id,
            preview_text=data.preview_text,
            title=data.title
        )

        db.add(post)
        db.commit()

        for tag_id in data.tags:
            post_tag = PostTag(
                post_id=post.id,
                tag_id=tag_id
            )

            db.add(post_tag)

        db.commit()

        return Response(status_code=201)
    except Exception as e:
        db.rollback()

        return HTTPException(status_code=500, detail=str(e))
