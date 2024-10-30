from app.db.models import BankAccount
from app.repositories.base import BasicRepository
from app.routers.internal.v1.schemas import BankAccountSchema


class BankAccountRepository(BasicRepository):
    """Repository for working with bank accounts."""

    _model = BankAccount
    _item_schema = BankAccountSchema
