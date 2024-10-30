from datetime import date
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional

from app.db.models import BankAccount, Customer, Transaction


class CustomerFilter(Filter):
    """Filtering the customer model."""

    id: Optional[int]  # noqa
    name__ilike: Optional[str]
    created_at__gte: Optional[date]
    created_at__lte: Optional[date]
    ordering: Optional[list[str]] = ['name']

    class Constants(Filter.Constants):
        model = Customer
        ordering_field_name = 'ordering'


class BankAccountFilter(Filter):
    """Filtering the bank account model."""

    id: Optional[int]  # noqa
    customer_id: Optional[int]
    customer: Optional[CustomerFilter] = FilterDepends(with_prefix("customer", CustomerFilter))
    balance: Optional[float]
    balance__gte: Optional[float]
    balance__lte: Optional[float]
    created_at__gte: Optional[date]
    created_at__lte: Optional[date]
    ordering: Optional[list[str]] = ['-created_at']

    class Constants(Filter.Constants):
        model = BankAccount
        ordering_field_name = 'ordering'


class TransactionFilter(Filter):
    """Filtering the transaction model."""

    id: Optional[int]  # noqa
    from_bank_account_id: Optional[int]
    to_bank_account_id: Optional[int]
    amount: Optional[float]
    amount__gte: Optional[float]
    amount__lte: Optional[float]
    type__ilike: Optional[str]
    from_bank_account: Optional[BankAccountFilter] = FilterDepends(with_prefix("from_bank_account", BankAccountFilter))
    to_bank_account: Optional[BankAccountFilter] = FilterDepends(with_prefix("to_bank_account", BankAccountFilter))
    created_at__gte: Optional[date]
    created_at__lte: Optional[date]
    ordering: Optional[list[str]] = ['-created_at']

    class Constants(Filter.Constants):
        model = Transaction
        ordering_field_name = 'ordering'
