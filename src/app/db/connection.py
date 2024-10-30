import inspect
import orjson
from contextlib import asynccontextmanager
from functools import wraps
from logging import Logger, getLogger
from sqlalchemy import MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.ext import asyncio as sa_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Any, AsyncIterator

from app.config import PROJECT_NAME, SETTINGS
from app.db.models.base import orjson_dumps


logger = getLogger(__name__)


def init_logging(logger_instance: Logger, description: str = '') -> Any:  # noqa
    """Logging the initialization of various dependencies at application startup."""

    def wrap(func):  # noqa
        @wraps(func)
        def init_log(*args, **kwargs):
            logger_instance.info(f'initialization: {description} starting')
            result = func(*args, **kwargs)
            logger_instance.info(f'initialization: {description} started')
            return result

        @wraps(func)
        async def async_init_log(*args, **kwargs):
            logger_instance.info(f'initialization: {description} starting')
            result = await func(*args, **kwargs)
            logger_instance.info(f'initialization: {description} started')
            return result

        if inspect.iscoroutinefunction(func):
            return async_init_log
        return init_log

    return wrap


def get_master_dsn(is_test: bool = False):
    master_dsn = URL.create(
        drivername=SETTINGS.DB.PROTOCOL,
        username=SETTINGS.DB.USER,
        password=SETTINGS.DB.PASSWORD,
        host=SETTINGS.DB.HOST,
        port=SETTINGS.DB.PORT,
        database=SETTINGS.DB.DATABASE,
    ).render_as_string(hide_password=False)

    if is_test:
        master_dsn += '_test'

    return master_dsn


POSTGRESQL_MASTER_DSN = get_master_dsn()


@init_logging(logger, 'database')
def init_db(long_operation: bool = False, is_test: bool = False) -> AsyncEngine:
    dsn = get_master_dsn(is_test)

    timeout_command = SETTINGS.DB.TIMEOUT_COMMAND * 100 if long_operation else SETTINGS.DB.TIMEOUT_COMMAND

    return sa_asyncio.create_async_engine(
        dsn,
        max_overflow=0,
        connect_args={
            'server_settings': {'application_name': PROJECT_NAME, 'timezone': 'utc'},
            'timeout': SETTINGS.DB.TIMEOUT_CONNECTION,
            'command_timeout': timeout_command,
        },
        pool_pre_ping=True,
        json_serializer=orjson_dumps,
        json_deserializer=orjson.loads,
    )


db = init_db()
Session = sessionmaker(bind=db, class_=sa_asyncio.AsyncSession, expire_on_commit=False)
metadata = MetaData(schema=SETTINGS.DB.SCHEMA)


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Provide a transactional scope around a series of operations."""

    async_session = Session()

    try:
        yield async_session
        await async_session.commit()
    except Exception:
        await async_session.rollback()
        raise
    finally:
        await async_session.close()
