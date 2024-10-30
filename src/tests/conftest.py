import asyncio
import json
import os
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer
from aiohttp.web import Request, Response
from alembic import command
from alembic.config import Config
from aresponses import ResponsesMockServer
from asyncio import AbstractEventLoop
from faker import Faker
from httpx import AsyncClient
from pathlib import Path
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from typing import Any, AsyncGenerator, Dict, Generator, Union
from yarl import URL

from app.db.connection import get_master_dsn
from app.db.models import BankAccount, Customer, User
from app.main import app
from app.repositories import BankAccountRepository, CustomerRepository, TransactionRepository
from app.services import BankAccountService, CustomerService, TransactionService
from app.utils.security import hash_password
from tests.constants import API_CREDENTIALS, INIT_CREATE_COUNT
from tests.utils import create_database, drop_database


faker = Faker()


def _run_upgrade(connection: AsyncConnection) -> None:
    base_dir = Path(__file__).resolve().parent.parent
    alembic_cfg = Config(os.path.join(base_dir, 'alembic.ini'))

    alembic_cfg.attributes['connection'] = connection
    command.upgrade(alembic_cfg, 'head')


@pytest.fixture(scope='session', autouse=True)
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def database(event_loop: AbstractEventLoop) -> AsyncGenerator[str, None]:
    db_url = get_master_dsn(is_test=True)
    await create_database(db_url)
    engine = create_async_engine(db_url, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(_run_upgrade)
    await engine.dispose()

    try:
        yield db_url
    finally:
        await drop_database(db_url)


@pytest.fixture(scope='session')
async def sqla_engine(database: str) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(database, poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest.fixture()
async def db_session(mocker: MockerFixture, sqla_engine: AsyncEngine) -> AsyncSession:
    """
    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.
    """
    connection = await sqla_engine.connect()
    trans = await connection.begin()

    session = AsyncSession(bind=connection, expire_on_commit=False)

    mocker.patch('sqlalchemy.orm.session.sessionmaker.__call__', return_value=session)

    async with session:
        yield session

        await trans.rollback()
        await connection.close()


class ResponsesMock(ResponsesMockServer):
    def response(self, data: Union[Dict[str, Any], str], status: int = 200) -> Response:
        headers = {'Content-Type': 'application/json'}

        if isinstance(data, dict):
            content = json.dumps(data, indent=4, ensure_ascii=False)
        elif isinstance(data, str):
            content = data
        else:
            raise TypeError(f'Invalid data type: {data}')

        return self.Response(text=content, headers=headers, status=status)


@pytest.fixture()
async def mock(event_loop: AbstractEventLoop) -> AsyncGenerator[ResponsesMock, None]:
    async with ResponsesMock(loop=event_loop) as server:
        yield server


@pytest.fixture()
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://testserver') as test_client:
        yield test_client


@pytest.fixture()
async def http_server_url() -> AsyncGenerator[URL, None]:
    router = web.RouteTableDef()

    @router.get('/test')
    @router.post('/test')
    @router.put('/test')
    @router.patch('/test')
    @router.delete('/test')
    async def ok(request: Request) -> Response:
        return web.json_response('ok')

    app = web.Application()
    app.add_routes(router)
    server = TestServer(app)
    await server.start_server()

    yield URL.build(scheme='http', host=server.host, port=server.port)
    await server.close()


@pytest.fixture()
async def customer_repo(db_session: AsyncSession) -> CustomerRepository:
    return CustomerRepository(session=db_session)


@pytest.fixture()
async def bank_account_repo(db_session: AsyncSession) -> BankAccountRepository:
    return BankAccountRepository(session=db_session)


@pytest.fixture()
async def transaction_repo(db_session: AsyncSession) -> TransactionRepository:
    return TransactionRepository(session=db_session)


@pytest.fixture()
def customer_service(customer_repo: CustomerRepository) -> CustomerService:
    return CustomerService(customer_repo)


@pytest.fixture()
def bank_account_service(bank_account_repo: BankAccountRepository) -> BankAccountService:
    return BankAccountService(bank_account_repo)


@pytest.fixture()
def transaction_service(transaction_repo: TransactionRepository) -> TransactionService:
    return TransactionService(transaction_repo)


@pytest.fixture(autouse=True)
async def create_service_user(db_session: AsyncSession):
    username, password = API_CREDENTIALS
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    db_session.add(new_user)


async def _generate_fake_customers(count: int):
    return [Customer(name=faker.name()) for _count in range(count)]


async def _generate_fake_bank_accounts(count: int, customer_repo: CustomerRepository):
    customers = await customer_repo.get_all()
    return [
        BankAccount(
            balance=faker.random_digit(),
            customer_id=customers[0].id,
        ) for _count in range(count)
    ]


@pytest.fixture(autouse=True)
async def setup_data(db_session: AsyncSession, customer_repo) -> None:
    customers = await _generate_fake_customers(count=INIT_CREATE_COUNT)
    db_session.add_all(customers)
    await db_session.commit()

    bank_accounts = await _generate_fake_bank_accounts(count=INIT_CREATE_COUNT, customer_repo=customer_repo)
    db_session.add_all(bank_accounts)
    await db_session.commit()
