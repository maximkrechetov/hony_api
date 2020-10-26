from .default_model import DefaultModel
from sqlalchemy import Column, Integer, String, ForeignKey, orm


class UserTag(DefaultModel):
    __tablename__ = 'user_tag'

    user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), index=True, nullable=False)

    tag = orm.relation('Tag')
    user = orm.relation('User')
