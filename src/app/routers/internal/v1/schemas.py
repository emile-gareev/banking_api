from datetime import datetime
from pydantic import NonNegativeFloat, PositiveFloat
from typing import List, Optional

from app.db.models import ORJSONModel


class BaseListSchema(ORJSONModel):
    count: int
    pages: int


class BaseItemSchema(ORJSONModel):
    id: int  # noqa

    class Config:
        orm_mode = True


class CustomerBaseSchema(ORJSONModel):
    name: str


class CustomerSchema(CustomerBaseSchema, BaseItemSchema):
    created_at: datetime
    updated_at: datetime


class CustomersListSchema(BaseListSchema):
    customers: List[Optional[CustomerSchema]]


class BankAccountBaseSchema(ORJSONModel):
    balance: NonNegativeFloat
    customer_id: int


class BankAccountSchema(BankAccountBaseSchema, BaseItemSchema):
    created_at: datetime
    updated_at: datetime


class BankAccountsListSchema(BaseListSchema):
    bank_accounts: List[Optional[BankAccountSchema]]


class BankAccountBalanceSchema(ORJSONModel):
    balance: float


class TransactionBaseSchema(ORJSONModel):
    from_bank_account_id: Optional[int]
    to_bank_account_id: Optional[int]
    amount: PositiveFloat
    type: str  # noqa


class TransactionSchema(TransactionBaseSchema, BaseItemSchema):
    created_at: datetime
    updated_at: datetime
    amount: float


class TransactionsListSchema(BaseListSchema):
    transactions: List[Optional[TransactionSchema]]


class TransactionTypesListSchema(ORJSONModel):
    types: List[tuple]
