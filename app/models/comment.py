from .default_model import DefaultModel
from sqlalchemy import Column, Integer, String, orm, ForeignKey


class Comment(DefaultModel):
    __tablename__ = 'comment'

    text = Column(String(512), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), index=True, nullable=False)
    parent_comment = Column(Integer, nullable=True)

    author = orm.relation('User')
    post = orm.relation('Post')
