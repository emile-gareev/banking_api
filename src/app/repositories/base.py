from abc import ABC
from sqlalchemy import distinct, func, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


class BasicRepository(ABC):
    _model = None
    _item_schema = None

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_all(self, page: int = 1, limit: Optional[int] = 25, filtering=None, extra_filters=None):
        """Get all raws with filtering, sorting and pagination applied."""

        query = select(self._model).distinct()

        if filtering:
            query = filtering.filter(query)
            query = filtering.sort(query)

        if extra_filters:
            or_condition = or_(*(getattr(self._model, _filter[0]) == _filter[1] for _filter in extra_filters))
            query = query.where(or_condition)

        if page and limit:
            offset = (page - 1) * limit
            query = query.limit(limit).offset(offset)

        result = await self._session.execute(query)
        return result.unique().scalars().all()

    async def total_count(self, filtering=None, extra_filters=None):
        """Get all raws count with filtering applied."""

        query = select(func.count(distinct(self._model.id))).select_from(self._model)
        if filtering:
            query = filtering.filter(query)

        if extra_filters:
            or_condition = or_(*(getattr(self._model, _filter[0]) == _filter[1] for _filter in extra_filters))
            query = query.where(or_condition)

        result = await self._session.execute(query)
        return result.scalar()

    async def get_by_id(self, _id: int, return_schema=False):
        """Get raw by its id."""

        query = select(self._model).where(self._model.id == _id)
        result = await self._session.scalars(query)
        instance = result.first()

        if instance and return_schema:
            return self._item_schema.from_orm(instance)

        return instance

    async def create_item(self, create_data):
        """Create new raw with returning its id."""

        result = await self._session.execute(insert(self._model).values(**create_data))
        return result.inserted_primary_key[0]

    async def save(self) -> None:
        await self._session.commit()
