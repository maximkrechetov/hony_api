from .default_model import DefaultModel
from sqlalchemy import Column, Integer, String, DateTime, func, orm
from app.database import db


class Comment(DefaultModel):
    __tablename__ = 'comment'

    text = Column(String(512), nullable=False)
    author_id = Column(Integer, ForeignKey('account.id'), index=True, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), index=True, nullable=False)
    parent_comment = Column(Integer, nullable=True)

    author = orm.relation('Account')
    post = orm.relation('Post')
