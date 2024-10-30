from logging import getLogger

from app.errors.custom_exception import NotFoundException
from app.repositories import BankAccountRepository
from app.services.base_service import BaseService

logger = getLogger(__file__)


class BankAccountService(BaseService):
    """Service for work with bank accounts."""

    def __init__(self, repository: BankAccountRepository) -> None:
        self._repository = repository

    async def get_balance(self, bank_account_id: int):
        bank_account = await self.get_item(bank_account_id)
        return bank_account.balance if bank_account else None

    async def get_bank_accounts_by_customer(self, page: int = 1, limit: int = 25, extra_filters: list = None):
        if bank_accounts := await self.get_list(page=page, limit=limit, extra_filters=extra_filters):
            return bank_accounts
        raise NotFoundException
