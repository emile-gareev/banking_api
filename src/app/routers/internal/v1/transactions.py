from fastapi import Depends, Response, status
from fastapi_filter import FilterDepends
from fastapi.routing import APIRouter

from app.enums import TransactionTypes
from app.dependencies.security import get_current_user
from app.dependencies.services import get_transaction_service
from app.errors.base import NotFoundError
from app.errors.custom_exception import NotFoundException
from app.repositories.security import UserSchema
from app.routers.error_shema import ErrorMessage
from app.routers.internal.v1.filters import TransactionFilter
from app.routers.internal.v1.schemas import (
    TransactionBaseSchema,
    TransactionSchema,
    TransactionsListSchema,
    TransactionTypesListSchema,
)
from app.services.transaction_service import TransactionService

router = APIRouter()


@router.get(
    '/',
    response_model=TransactionsListSchema,
    responses={
        200: {'model': TransactionsListSchema, 'description': 'List of all transactions'},
    },
)
async def list_transactions(
    page: int = 1,
    limit: int = 25,
    user: UserSchema = Depends(get_current_user),
    filtering: TransactionFilter = FilterDepends(TransactionFilter),
    service: TransactionService = Depends(get_transaction_service),
):
    """Getting a list of all transactions."""

    total_count = await service.get_count(filtering=filtering)
    transactions = await service.get_list(page=page, limit=limit, filtering=filtering)
    pages = round(total_count / limit)
    return {'count': total_count, 'pages': pages if pages else 1, 'transactions': transactions}


@router.post(
    '/',
    responses={
        201: {'model': TransactionBaseSchema, 'description': 'Creating a record of a transaction'},
    },
)
async def create_transaction(
    input_data: TransactionBaseSchema,
    response: Response,
    user: UserSchema = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    """Creating new transaction."""

    response.status_code = status.HTTP_201_CREATED
    return await service.create_item(input_data)


@router.get(
    '/transaction_types/',
    responses={
        200: {'model': TransactionTypesListSchema, 'description': 'List of all transaction types'},
    },
)
async def list_transaction_types(
    user: UserSchema = Depends(get_current_user),
):
    """Getting a list of all transaction types."""

    return [(t.name, t.value) for t in TransactionTypes]


@router.get(
    '/{transaction_id}/',
    response_model=TransactionSchema,
    responses={
        200: {'model': TransactionSchema, 'description': 'Transaction'},
        404: {'model': ErrorMessage, 'description': 'Transaction not found'},
    },
)
async def get_transaction(
    transaction_id: int,
    user: UserSchema = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    """Getting information of specific transaction."""

    try:
        transaction_data = await service.get_item(transaction_id)
    except NotFoundException:
        raise NotFoundError

    return transaction_data
