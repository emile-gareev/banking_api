from app.db.models import Transaction
from app.enums import TransactionTypes
from app.errors.base import ItemNotFoundError, NotEnoughEquity
from app.errors.custom_exception import BadRequestException
from app.repositories import BankAccountRepository
from app.repositories.base import BasicRepository
from app.routers.internal.v1.schemas import TransactionSchema


class TransactionRepository(BasicRepository):
    """Repository for working with transactions."""

    _model = Transaction
    _item_schema = TransactionSchema

    async def create_item(self, create_data):
        """Create new transaction."""

        bank_account_repository = BankAccountRepository(session=self._session)

        transaction_type = create_data.get('type')
        if transaction_type not in TransactionTypes.as_dict():
            raise BadRequestException
        if transaction_type == TransactionTypes.TRANSFER.name:
            account_from = await bank_account_repository.get_by_id(create_data.get('from_bank_account_id'))
            if not account_from:
                raise ItemNotFoundError('from_bank_account_id')
            account_to = await bank_account_repository.get_by_id(create_data.get('to_bank_account_id'))
            if not account_to:
                raise ItemNotFoundError('to_bank_account_id')
            if account_from.balance < create_data.get('amount'):
                raise NotEnoughEquity
            account_from.balance -= create_data.get('amount')
            account_to.balance += create_data.get('amount')
        elif transaction_type == TransactionTypes.DEPOSIT.name:
            account_to = await bank_account_repository.get_by_id(create_data.get('to_bank_account_id'))
            if not account_to:
                raise ItemNotFoundError('to_bank_account_id')
            account_to.balance += create_data.get('amount')
        elif transaction_type == TransactionTypes.WITHDRAWAL.name:
            account_from = await bank_account_repository.get_by_id(create_data.get('from_bank_account_id'))
            if not account_from:
                raise ItemNotFoundError('from_bank_account_id')
            if account_from.balance < create_data.get('amount'):
                raise NotEnoughEquity
            account_from.balance -= create_data.get('amount')

        return await super().create_item(create_data)
