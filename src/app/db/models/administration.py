from sqlalchemy import Boolean, Column, Integer, String

from app.db.models.base import Base


class User(Base):
    """User for API connection."""

    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)  # noqa
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(100))
    name = Column(String(100))
    is_active = Column(Boolean, default=True, nullable=False)
