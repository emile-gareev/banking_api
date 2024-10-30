from fastapi import Depends, Response, status
from fastapi_filter import FilterDepends
from fastapi.routing import APIRouter

from app.dependencies.security import get_current_user
from app.dependencies.services import get_bank_account_service, get_customer_service, get_transaction_service
from app.errors.base import ItemNotFoundError, NotFoundError
from app.errors.custom_exception import NotFoundException
from app.repositories.security import UserSchema
from app.routers.error_shema import ErrorMessage
from app.routers.internal.v1.filters import BankAccountFilter
from app.routers.internal.v1.schemas import (
    BankAccountBalanceSchema,
    BankAccountBaseSchema,
    BankAccountSchema,
    BankAccountsListSchema,
    TransactionsListSchema,
)
from app.services import BankAccountService, CustomerService, TransactionService

router = APIRouter()


@router.get(
    '/',
    response_model=BankAccountsListSchema,
    responses={
        200: {'model': BankAccountsListSchema, 'description': 'List of all bank accounts'},
    },
)
async def list_bank_accounts(
    page: int = 1,
    limit: int = 25,
    user: UserSchema = Depends(get_current_user),
    filtering: BankAccountFilter = FilterDepends(BankAccountFilter),
    service: BankAccountService = Depends(get_bank_account_service),
):
    """Getting a list of all bank accounts."""

    total_count = await service.get_count(filtering=filtering)
    bank_accounts = await service.get_list(page=page, limit=limit, filtering=filtering)
    pages = round(total_count / limit)
    return {'count': total_count, 'pages': pages if pages else 1, 'bank_accounts': bank_accounts}


@router.post(
    '/',
    responses={
        201: {'model': BankAccountSchema, 'description': 'Creating a record of a bank account'},
    },
)
async def create_bank_account(
    input_data: BankAccountBaseSchema,
    response: Response,
    user: UserSchema = Depends(get_current_user),
    service: BankAccountService = Depends(get_bank_account_service),
    customer_service: CustomerService = Depends(get_customer_service),
):
    """Creating new bank account."""

    try:
        await customer_service.get_item(input_data.customer_id)
    except NotFoundException:
        raise ItemNotFoundError(item_name='customer_id')

    response.status_code = status.HTTP_201_CREATED
    return await service.create_item(input_data)


@router.get(
    '/{bank_account_id}/balance/',
    response_model=BankAccountBalanceSchema,
    responses={
        200: {'model': BankAccountBalanceSchema, 'description': 'Bank account balance'},
        404: {'model': ErrorMessage, 'description': 'Bank account not found'},
    },
)
async def get_bank_account_balance(
    bank_account_id: int,
    user: UserSchema = Depends(get_current_user),
    service: BankAccountService = Depends(get_bank_account_service),
):
    """Getting information of specific bank account balance."""

    try:
        balance = await service.get_balance(bank_account_id)
    except NotFoundException:
        raise NotFoundError

    return {'balance': balance}


@router.get(
    '/{bank_account_id}/transactions/',
    response_model=TransactionsListSchema,
    responses={
        200: {'model': TransactionsListSchema, 'description': 'Bank account transaction history'},
        404: {'model': ErrorMessage, 'description': 'Bank account not found'},
    },
)
async def get_transaction_history(
    bank_account_id: int,
    page: int = 1,
    limit: int = 25,
    user: UserSchema = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    """Getting information for all transactions of specific bank account."""

    try:
        total_count = await service.get_count(
            extra_filters=[('from_bank_account_id', bank_account_id), ('to_bank_account_id', bank_account_id)],
        )
        transactions = await service.get_transactions_by_bank_account(
            page,
            limit,
            extra_filters=[('from_bank_account_id', bank_account_id), ('to_bank_account_id', bank_account_id)],
        )
        pages = round(total_count / limit)
    except NotFoundException:
        raise NotFoundError

    return {'count': total_count, 'pages': pages if pages else 1, 'transactions': transactions}


@router.get(
    '/{bank_account_id}/',
    response_model=BankAccountSchema,
    responses={
        200: {'model': BankAccountSchema, 'description': 'Bank account'},
        404: {'model': ErrorMessage, 'description': 'Bank account not found'},
    },
)
async def get_bank_account(
    bank_account_id: int,
    user: UserSchema = Depends(get_current_user),
    service: BankAccountService = Depends(get_bank_account_service),
):
    """Getting information of specific bank account."""

    try:
        bank_account_data = await service.get_item(bank_account_id)
    except NotFoundException:
        raise NotFoundError

    return bank_account_data
