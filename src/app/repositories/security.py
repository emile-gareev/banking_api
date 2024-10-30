from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.models import ORJSONModel, User


class UserSchema(ORJSONModel):
    class Config:
        use_enum_values = True
        orm_mode = True

    id: int  # noqa
    username: str
    password: str
    email: Optional[str]
    name: Optional[str]
    is_active: bool


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_user_by_username(self, username: str) -> Optional[UserSchema]:
        query = select(User).where(User.username == username)
        result = await self._session.scalars(query)
        user = result.first()

        return UserSchema.from_orm(user) if user else None

    async def save(self) -> None:
        await self._session.commit()
