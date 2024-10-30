from logging import getLogger

from app.errors.custom_exception import NotFoundException
from app.repositories import TransactionRepository
from app.services.base_service import BaseService

logger = getLogger(__file__)


class TransactionService(BaseService):
    """Service for work with transactions."""

    def __init__(self, repository: TransactionRepository) -> None:
        self._repository = repository

    async def get_transactions_by_bank_account(self, page: int = 1, limit: int = 25, extra_filters: list = None):
        if transactions := await self.get_list(page=page, limit=limit, extra_filters=extra_filters):
            return transactions
        raise NotFoundException
