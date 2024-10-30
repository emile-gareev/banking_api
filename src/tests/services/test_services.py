import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import BankAccount, Customer, Transaction
from app.enums import TransactionTypes
from app.errors.base import NotEnoughEquity
from app.services import BankAccountService, CustomerService, TransactionService
from tests.conftest import faker
from tests.constants import INIT_CREATE_COUNT


async def _get_item_from_db(db_session: AsyncSession, model):
    db_result = await db_session.execute(select(model))
    db_item = db_result.fetchone()[0]
    assert db_item
    return db_item


async def test_list_customers(customer_service: CustomerService):
    customers_count = await customer_service.get_count()
    assert customers_count == INIT_CREATE_COUNT

    all_customers = await customer_service.get_list(page=1, limit=10)
    assert len(all_customers) == INIT_CREATE_COUNT


async def test_get_customer(db_session: AsyncSession, customer_service: CustomerService):
    db_customer = await _get_item_from_db(db_session, Customer)

    customer_from_service = await customer_service.get_item(db_customer.id)
    assert customer_from_service
    assert customer_from_service.id == db_customer.id


async def test_create_customer(db_session: AsyncSession, customer_service: CustomerService):
    create_data = {'name': faker.name()}
    created_customer = await customer_service.create_item(create_data)
    assert created_customer


async def test_list_bank_accounts(bank_account_service: BankAccountService):
    bank_accounts_count = await bank_account_service.get_count()
    assert bank_accounts_count == INIT_CREATE_COUNT

    all_bank_accounts = await bank_account_service.get_list(page=1, limit=10)
    assert len(all_bank_accounts) == INIT_CREATE_COUNT


async def test_get_bank_account(db_session: AsyncSession, bank_account_service: BankAccountService):
    db_bank_account = await _get_item_from_db(db_session, BankAccount)

    bank_account_from_service = await bank_account_service.get_item(db_bank_account.id)
    assert bank_account_from_service
    assert bank_account_from_service.id == db_bank_account.id


async def test_create_bank_account(db_session: AsyncSession, bank_account_service: BankAccountService):
    customer = await _get_item_from_db(db_session, Customer)
    create_data = {'customer_id': customer.id, 'balance': faker.random_digit()}
    created_bank_account = await bank_account_service.create_item(create_data)
    assert created_bank_account


async def test_transactions(
        db_session: AsyncSession, transaction_service: TransactionService, bank_account_service: BankAccountService,
):
    bank_account = await _get_item_from_db(db_session, BankAccount)
    balance = await bank_account_service.get_balance(bank_account.id)

    create_data = {
        'from_bank_account_id': bank_account.id,
        'amount': balance - 1,
        'type': TransactionTypes.WITHDRAWAL.name,
    }
    created_transaction = await transaction_service.create_item(create_data)
    assert created_transaction

    create_data = {
        'from_bank_account_id': bank_account.id,
        'amount': balance,
        'type': TransactionTypes.WITHDRAWAL.name,
    }
    with pytest.raises(NotEnoughEquity) as exc_info:
        await transaction_service.create_item(create_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == {'code': 'BAD_REQUEST', 'message': 'There is not enough equity in the account'}

    transactions_count = await transaction_service.get_count()
    assert transactions_count == 1

    all_transactions = await transaction_service.get_list(page=1, limit=10)
    assert len(all_transactions) == 1

    db_transaction = await _get_item_from_db(db_session, Transaction)

    transaction_from_service = await transaction_service.get_item(db_transaction.id)
    assert transaction_from_service
    assert transaction_from_service.id == db_transaction.id
