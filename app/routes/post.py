from datetime import datetime
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from app.models import Post, User, Tag, PostTag
from app.database import get_db
from app.auth import get_current_user
from app.schemas.post import PostCreateUpdateModel, PostRetrieveModel


router = APIRouter()


@router.post('/create')
async def create(
    data: PostCreateUpdateModel,
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


@router.put('/update')
async def update_post(
    data: PostCreateUpdateModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates Post instance
    :param data: must be PostCreateModel comparable
    :param current_user: Current authenticated user
    :param db: Session instance
    :return: 204 Updated
    """
    try:
        post = db.query(Post).filter_by(id=data.id).first()

        if not post:
            return HTTPException(status_code=404, detail='Post not found')

        post.preview_text = data.preview_text
        post.text = data.text
        post.title = data.title
        post.cover = data.cover
        post.updated_at = datetime.now()

        if data.tags:
            post_tags = db.query(PostTag).filter_by(post_id=post.id).all()
            existing_post_tag_ids = []

            for tag in post_tags:
                if tag.id not in data.tags:
                    db.delete(tag)
                    continue

                existing_post_tag_ids.append(tag.id)

            for tag_id in data.tags:
                if tag_id not in existing_post_tag_ids:
                    new_post_tag = PostTag(
                        post_id=post.id,
                        tag_id=tag_id
                    )

                    db.add(new_post_tag)

        db.add(post)
        db.commit()

        return Response(status_code=204)

    except Exception as e:
        db.rollback()

        return HTTPException(status_code=500, detail=str(e))


