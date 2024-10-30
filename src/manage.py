import asyncio
import typer
import uvicorn
from functools import wraps
from IPython import embed
from typing import Any, Awaitable, Callable, TypeVar
from typing_extensions import ParamSpec

from app.commands.base import create_service_user
from app.config import SETTINGS


typer_app = typer.Typer()

T = TypeVar('T')
P = ParamSpec('P')  # noqa


def coro(func: Callable[P, Awaitable[T]]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@typer_app.command()
def shell() -> None:
    embed()


@typer_app.command()
def runserver() -> None:
    uvicorn.run(**SETTINGS.UVICORN.dict())


@typer_app.command()
@coro
async def create_user(username: str, password: str):
    await create_service_user(username, password)


if __name__ == '__main__':
    typer_app()
