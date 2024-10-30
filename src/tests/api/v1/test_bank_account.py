from http import HTTPStatus
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import TransactionTypes
from app.repositories import BankAccountRepository, CustomerRepository
from tests.conftest import faker
from tests.constants import API_CREDENTIALS


async def test_get_all(async_client: AsyncClient, db_session: AsyncSession, bank_account_repo: BankAccountRepository):
    no_auth_response = await async_client.request('GET', '/api/v1/bank_accounts/')
    assert no_auth_response.status_code == HTTPStatus.UNAUTHORIZED

    auth_response = await async_client.request('GET', '/api/v1/bank_accounts/', auth=API_CREDENTIALS)
    assert auth_response.status_code == HTTPStatus.OK

    bank_accounts_in_db = await bank_account_repo.get_all()
    auth_response_data = auth_response.json()

    assert auth_response_data['count'] == len(bank_accounts_in_db)


async def test_get_by_id(async_client: AsyncClient, bank_account_repo: BankAccountRepository):
    bank_accounts = await bank_account_repo.get_all()
    assert bank_accounts[0]

    bank_account_id: int = bank_accounts[1].id

    no_auth_response = await async_client.request('GET', '/api/v1/bank_accounts/401/')
    assert no_auth_response.status_code == HTTPStatus.UNAUTHORIZED

    ok_response = await async_client.request('GET', f'/api/v1/bank_accounts/{bank_account_id}/', auth=API_CREDENTIALS)
    assert ok_response.status_code == HTTPStatus.OK

    not_found_response = await async_client.request('GET', '/api/v1/bank_accounts/404/', auth=API_CREDENTIALS)
    assert not_found_response.status_code == HTTPStatus.NOT_FOUND


async def test_create_item(async_client: AsyncClient, customer_repo: CustomerRepository):
    customers = await customer_repo.get_all()
    customer_id: int = customers[0].id
    create_data = {'customer_id': customer_id, 'balance': faker.random_digit()}

    response = await async_client.request('POST', '/api/v1/bank_accounts/', auth=API_CREDENTIALS, json=create_data)
    assert response.status_code == HTTPStatus.CREATED


async def test_get_balance(async_client: AsyncClient, bank_account_repo: BankAccountRepository):
    bank_accounts = await bank_account_repo.get_all()
    bank_account_id: int = bank_accounts[0].id

    response = await async_client.request(
        'GET',
        f'/api/v1/bank_accounts/{bank_account_id}/balance/',
        auth=API_CREDENTIALS,
    )
    assert response.json().get('balance') >= 0
    assert isinstance(response.json().get('balance'), float)


async def test_get_transactions(async_client: AsyncClient, bank_account_repo: BankAccountRepository):
    bank_accounts = await bank_account_repo.get_all()
    bank_account_id: int = bank_accounts[0].id

    create_data = {
        'to_bank_account_id': bank_account_id,
        'amount': faker.random_digit(),
        'type': TransactionTypes.DEPOSIT.name,
    }
    await async_client.request('POST', '/api/v1/transactions/', auth=API_CREDENTIALS, json=create_data)

    response = await async_client.request(
        'GET',
        f'/api/v1/bank_accounts/{bank_account_id}/transactions/',
        auth=API_CREDENTIALS,
    )
    assert response.json().get('count') == 1
