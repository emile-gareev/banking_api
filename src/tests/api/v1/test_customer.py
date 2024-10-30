from http import HTTPStatus
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import CustomerRepository
from tests.conftest import faker
from tests.constants import API_CREDENTIALS, INIT_CREATE_COUNT


async def test_get_all(async_client: AsyncClient, db_session: AsyncSession, customer_repo: CustomerRepository):
    no_auth_response = await async_client.request('GET', '/api/v1/customers/')
    assert no_auth_response.status_code == HTTPStatus.UNAUTHORIZED

    auth_response = await async_client.request('GET', '/api/v1/customers/', auth=API_CREDENTIALS)
    assert auth_response.status_code == HTTPStatus.OK

    customers_in_db = await customer_repo.get_all()
    auth_response_data = auth_response.json()

    assert auth_response_data['count'] == len(customers_in_db)


async def test_get_by_id(async_client: AsyncClient, customer_repo: CustomerRepository):
    customers = await customer_repo.get_all()
    assert customers[0]

    customer_id: int = customers[1].id

    no_auth_response = await async_client.request('GET', '/api/v1/customers/401/')
    assert no_auth_response.status_code == HTTPStatus.UNAUTHORIZED

    ok_response = await async_client.request('GET', f'/api/v1/customers/{customer_id}/', auth=API_CREDENTIALS)
    assert ok_response.status_code == HTTPStatus.OK

    not_found_response = await async_client.request('GET', '/api/v1/customers/404/', auth=API_CREDENTIALS)
    assert not_found_response.status_code == HTTPStatus.NOT_FOUND


async def test_create_item(async_client: AsyncClient):
    create_data = {'name': faker.name()}

    response = await async_client.request('POST', '/api/v1/customers/', auth=API_CREDENTIALS, json=create_data)
    assert response.status_code == HTTPStatus.CREATED


async def test_get_bank_accounts(async_client: AsyncClient, customer_repo: CustomerRepository):
    customers = await customer_repo.get_all()
    customer_id: int = customers[0].id

    response = await async_client.request(
        'GET',
        f'/api/v1/customers/{customer_id}/bank_accounts/',
        auth=API_CREDENTIALS,
    )
    assert response.json().get('count') == INIT_CREATE_COUNT
