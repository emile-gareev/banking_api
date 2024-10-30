from fastapi import Depends, Response, status
from fastapi_filter import FilterDepends
from fastapi.routing import APIRouter

from app.dependencies.security import get_current_user
from app.dependencies.services import get_bank_account_service, get_customer_service
from app.errors.base import NotFoundError
from app.errors.custom_exception import NotFoundException
from app.repositories.security import UserSchema
from app.routers.error_shema import ErrorMessage
from app.routers.internal.v1.filters import CustomerFilter
from app.routers.internal.v1.schemas import (
    BankAccountsListSchema,
    CustomerBaseSchema,
    CustomerSchema,
    CustomersListSchema,
)
from app.services import BankAccountService, CustomerService


router = APIRouter()


@router.get(
    '/',
    response_model=CustomersListSchema,
    responses={
        200: {'model': CustomersListSchema, 'description': 'List of all customers'},
    },
)
async def list_customers(
    page: int = 1,
    limit: int = 25,
    user: UserSchema = Depends(get_current_user),
    filtering: CustomerFilter = FilterDepends(CustomerFilter),
    service: CustomerService = Depends(get_customer_service),
):
    """Getting a list of all customers."""

    total_count = await service.get_count(filtering=filtering)
    customers = await service.get_list(page=page, limit=limit, filtering=filtering)
    pages = round(total_count / limit)
    return {'count': total_count, 'pages': pages if pages else 1, 'customers': customers}


@router.post(
    '/',
    responses={
        201: {'model': CustomerSchema, 'description': 'Creating a record of a customer'},
    },
)
async def create_customer(
    input_data: CustomerBaseSchema,
    response: Response,
    user: UserSchema = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    """Creating new customer."""

    response.status_code = status.HTTP_201_CREATED
    return await service.create_item(input_data)


@router.get(
    '/{customer_id}/',
    response_model=CustomerSchema,
    responses={
        200: {'model': CustomerSchema, 'description': 'Customer'},
        404: {'model': ErrorMessage, 'description': 'Customer not found'},
    },
)
async def get_customer(
    customer_id: int,
    user: UserSchema = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    """Getting information of specific customer."""

    try:
        customer_data = await service.get_item(customer_id)
    except NotFoundException:
        raise NotFoundError

    return customer_data


@router.get(
    '/{customer_id}/bank_accounts/',
    response_model=BankAccountsListSchema,
    responses={
        200: {'model': BankAccountsListSchema, 'description': 'Customer bank accounts'},
        404: {'model': ErrorMessage, 'description': 'Customer not found'},
    },
)
async def get_customer_bank_accounts(
    customer_id: int,
    page: int = 1,
    limit: int = 25,
    user: UserSchema = Depends(get_current_user),
    service: BankAccountService = Depends(get_bank_account_service),
):
    """Getting information for all bank accounts of specific customer."""

    try:
        total_count = await service.get_count(extra_filters=[('customer_id', customer_id)])
        bank_accounts = await service.get_bank_accounts_by_customer(
            page,
            limit,
            extra_filters=[('customer_id', customer_id)],
        )
        pages = round(total_count / limit)
    except NotFoundException:
        raise NotFoundError

    return {'count': total_count, 'pages': pages if pages else 1, 'bank_accounts': bank_accounts}
