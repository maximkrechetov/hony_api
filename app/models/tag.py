from .default_model import DefaultModel
from sqlalchemy import Column, Integer, String, DateTime, func, orm
from app.database import db


class Tag(DefaultModel):
    __tablename__ = 'tag'

    title = Column(String(64), nullable=False)
    is_active = Column(Boolean, default=True)
