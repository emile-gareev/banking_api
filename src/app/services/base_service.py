from abc import ABC
from fastapi_filter.contrib.sqlalchemy import Filter
from logging import getLogger
from typing import Union

from app.errors.base import WrongTransactionType
from app.db.models import ORJSONModel
from app.errors.custom_exception import BadRequestException, NotFoundException

logger = getLogger(__file__)


class BaseService(ABC):
    """Base abstract service."""

    _repository = None

    async def get_count(self, filtering: Filter = None, extra_filters=None):
        return await self._repository.total_count(filtering=filtering, extra_filters=extra_filters)

    async def get_list(self, page: int, limit: int, filtering=None, extra_filters=None):
        return await self._repository.get_all(page, limit, filtering=filtering, extra_filters=extra_filters)

    async def get_item(self, _id: int):
        instance = await self._repository.get_by_id(_id, return_schema=False)
        if not instance:
            raise NotFoundException

        return instance

    async def create_item(self, input_data: Union[ORJSONModel, dict]):
        if isinstance(input_data, ORJSONModel):
            input_dict: dict = input_data.dict()
        else:
            input_dict = input_data

        try:
            instance_id = await self._repository.create_item(input_dict)
        except BadRequestException:
            raise WrongTransactionType

        return await self.get_item(instance_id) if instance_id else None
