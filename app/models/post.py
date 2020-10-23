from .default_model import DefaultModel
from sqlalchemy import Column, Integer, String, Text, ForeignKey, orm


class Post(DefaultModel):
    __tablename__ = 'post'

    text = Column(Text, nullable=False)
    title = Column(String(128), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    preview_text = Column(String(300), nullable=False)
    cover = Column(String(64), nullable=True)

    author = orm.relation('User')
