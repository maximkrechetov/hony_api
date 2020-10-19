from .default_model import DefaultModel
from sqlalchemy import Column, Integer, String, DateTime, func, orm
from app.database import db


class Post(DefaultModel):
    __tablename__ = 'post'

    text = Column(String(512), nullable=False)
    title = Column(String(128), nullable=False)
    author_id = Column(Integer, ForeignKey('account.id'), index=True, nullable=False)

    author = orm.relation('Account')
