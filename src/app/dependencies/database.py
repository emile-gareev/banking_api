from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterator

from app.db.connection import session_scope


async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_scope() as session:
        yield session
