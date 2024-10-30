from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from logging import getLogger

from app.config import SETTINGS
from app.routers.internal.v1.bank_accounts import router as bank_accounts_router
from app.routers.internal.v1.customers import router as customers_router
from app.routers.internal.v1.transactions import router as transactions_router


logger = getLogger('elk')


def init_routes(app_: FastAPI) -> None:
    app_.include_router(bank_accounts_router, prefix='/api/v1/bank_accounts', tags=['Bank accounts'])
    app_.include_router(customers_router, prefix='/api/v1/customers', tags=['Customers'])
    app_.include_router(transactions_router, prefix='/api/v1/transactions', tags=['Transactions'])


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=SETTINGS.service_name,
        default_response_class=ORJSONResponse,
        docs_url=f'{SETTINGS.API.ROOT}/docs' if SETTINGS.API.DOCS_ENABLED else None,
        openapi_url=f'{SETTINGS.API.ROOT}/docs/openapi.json' if SETTINGS.API.DOCS_ENABLED else None,
        redoc_url=f'{SETTINGS.API.ROOT}/redocs' if SETTINGS.API.DOCS_ENABLED else None,
        version=SETTINGS.API.VERSION,
    )

    init_routes(app_)
    return app_


app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('shutdown')
async def shutdown() -> None:
    logger.warning('Shutdown')
