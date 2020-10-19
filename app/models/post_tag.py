from .default_model import DefaultModel
from sqlalchemy import Column, Integer, String, DateTime, func, orm
from app.database import db


class PostTag(DefaultModel):
    __tablename__ = 'post_tag'

    post_id = Column(Integer, ForeignKey('post.id'), index=True, nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), index=True, nullable=False)

    tag = orm.relation('Tag')
    post = orm.relation('Post')
