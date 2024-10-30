import pytest
from _pytest.fixtures import SubRequest
from async_asgi_testclient import TestClient
from pytest_mock import MockerFixture

from app import main
from app.config import SETTINGS
from app.main import create_app


pytestmark = pytest.mark.asyncio


@pytest.fixture()
def show_docs_toggle(request: SubRequest, mocker: MockerFixture) -> bool:
    return mocker.patch.object(SETTINGS.API, "DOCS_ENABLED", request.param)


@pytest.fixture()
async def client(show_docs_toggle: bool) -> TestClient:
    app_ = create_app()
    async with TestClient(app_) as client:
        yield client


@pytest.mark.parametrize(
    ("url_path", "show_docs_toggle"),
    [
        (main.app.docs_url, True),
        (main.app.openapi_url, True),
        (main.app.redoc_url, True),
    ],
    indirect=["show_docs_toggle"],
)
async def test_docs_enabled(
    client: TestClient,
    url_path: str,
    show_docs_toggle: bool,
) -> None:
    response = await client.get(path=url_path)
    assert response.status_code == 200, response.text

    if url_path == main.app.openapi_url:
        assert response.json()["info"]["version"] == SETTINGS.API.VERSION


@pytest.mark.parametrize(
    ("url_path", "show_docs_toggle"),
    [
        (main.app.docs_url, False),
        (main.app.openapi_url, False),
        (main.app.redoc_url, False),
    ],
    indirect=["show_docs_toggle"],
)
async def test_docs_disabled(
    client: TestClient,
    url_path: str,
    show_docs_toggle: bool,
) -> None:
    response = await client.get(path=url_path)
    assert response.status_code == 404, response.text
