from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_session
from app.repositories import BankAccountRepository, CustomerRepository, TransactionRepository
from app.repositories.security import UserRepository


def get_customer_repository(session: AsyncSession = Depends(get_session)) -> CustomerRepository:
    return CustomerRepository(session)


def get_bank_account_repository(session: AsyncSession = Depends(get_session)) -> BankAccountRepository:
    return BankAccountRepository(session)


def get_transaction_repository(session: AsyncSession = Depends(get_session)) -> TransactionRepository:
    return TransactionRepository(session)


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)
