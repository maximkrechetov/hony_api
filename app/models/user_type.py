from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base


class UserType(Base):
    __tablename__ = 'user_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    alias = Column(String(32), nullable=False)
    title = Column(String(32), nullable=False)
    comment_limit = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())
