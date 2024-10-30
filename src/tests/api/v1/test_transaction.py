from http import HTTPStatus
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import TransactionTypes
from app.repositories import BankAccountRepository, TransactionRepository
from tests.constants import API_CREDENTIALS


async def test_get_all(async_client: AsyncClient, db_session: AsyncSession, transaction_repo: TransactionRepository):
    no_auth_response = await async_client.request('GET', '/api/v1/transactions/')
    assert no_auth_response.status_code == HTTPStatus.UNAUTHORIZED

    auth_response = await async_client.request('GET', '/api/v1/transactions/', auth=API_CREDENTIALS)
    assert auth_response.status_code == HTTPStatus.OK

    transactions_in_db = await transaction_repo.get_all()
    auth_response_data = auth_response.json()

    assert auth_response_data['count'] == len(transactions_in_db)


async def test_create_item(async_client: AsyncClient, bank_account_repo: BankAccountRepository):
    bank_accounts = await bank_account_repo.get_all()
    bank_account_id: int = bank_accounts[0].id

    response = await async_client.request(
        'GET',
        f'/api/v1/bank_accounts/{bank_account_id}/balance/',
        auth=API_CREDENTIALS,
    )
    balance = response.json().get('balance')

    create_data = {
        'from_bank_account_id': bank_account_id,
        'amount': balance,
        'type': TransactionTypes.WITHDRAWAL.name,
    }

    response = await async_client.request('POST', '/api/v1/transactions/', auth=API_CREDENTIALS, json=create_data)
    assert response.status_code == HTTPStatus.CREATED

    no_auth_response = await async_client.request('GET', '/api/v1/transactions/401/')
    assert no_auth_response.status_code == HTTPStatus.UNAUTHORIZED

    ok_response = await async_client.request(
        'GET',
        f'/api/v1/transactions/{response.json().get("id")}/',
        auth=API_CREDENTIALS,
    )
    assert ok_response.status_code == HTTPStatus.OK

    not_found_response = await async_client.request('GET', '/api/v1/transactions/404/', auth=API_CREDENTIALS)
    assert not_found_response.status_code == HTTPStatus.NOT_FOUND


async def test_get_transaction_types(async_client: AsyncClient):
    response = await async_client.request('GET', '/api/v1/transactions/transaction_types/', auth=API_CREDENTIALS)
    assert isinstance(response.json(), list)
    assert len(TransactionTypes) == len(response.json())
