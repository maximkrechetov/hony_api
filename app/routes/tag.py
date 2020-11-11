from fastapi import APIRouter, Depends, Response, HTTPException
from app.models import User, Tag, UserTag
from app.database import get_db
from app.auth import get_current_user
from app.schemas.tag import TagModel, SubscribeModel
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.post('/create')
async def create_tag(
    data: TagModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create new tag
    :param data: tag_id to create
    :param current_user: Current User instance
    :param db: db instance
    :return: 201 Created
    """
    tag = db.query(Tag).filter_by(title=data.title).first()

    if not tag:
        tag = Tag(
            title=data.title
        )

        db.add(tag)
        db.commit()

        return Response(status_code=201)

    raise HTTPException(status_code=409, detail="Tag already exists")


@router.post('/subscribe')
async def subscribe_tag(
    data: SubscribeModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Subscribe to tag
    :param data: tag_id to subscribe
    :param current_user: Current User instance
    :param db: db instance
    :return: 201 Created
    """
    user_tag = db.query(UserTag).filter_by(
        user_id=current_user.id,
        tag_id=data.tag_id
    ).first()

    if not user_tag:
        user_tag = UserTag(
            tag_id=data.tag_id,
            user_id=current_user.id
        )

        db.add(user_tag)
        db.commit()

        return Response(status_code=201)

    raise HTTPException(status_code=409, detail="Already subscribed")


@router.delete('/unsubscribe')
async def unsubscribe_tag(
    data: SubscribeModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Unsubscribe from tag
    :param data: tag_id to unsubscribe
    :param current_user: Current User instance
    :param db: db instance
    :return: 204 No Content
    """
    user_tag = db.query(UserTag).filter_by(
        user_id=current_user.id,
        tag_id=data.tag_id
    ).first()

    if not user_tag:
        raise HTTPException(status_code=404, detail="You are not subscribed already")

    db.delete(user_tag)
    db.commit()

    return Response(status_code=204)
