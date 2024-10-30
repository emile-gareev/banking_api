from datetime import datetime
from sqlalchemy import Column, DateTime, sql
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimeMixin:
    updated_at = Column(
        DateTime(timezone=False),
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
        server_default=sql.func.now(),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        server_default=sql.func.now(),
        nullable=False,
    )
