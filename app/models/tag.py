from .default_model import DefaultModel
from sqlalchemy import Column, String, Boolean


class Tag(DefaultModel):
    __tablename__ = 'tag'

    title = Column(String(64), nullable=False)
    is_active = Column(Boolean, default=True)
