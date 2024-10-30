from fastapi import Depends

from app.dependencies.repository import get_bank_account_repository, get_customer_repository, get_transaction_repository
from app.repositories import BankAccountRepository, CustomerRepository, TransactionRepository
from app.services import BankAccountService, CustomerService, TransactionService


def get_customer_service(repository: CustomerRepository = Depends(get_customer_repository)) -> CustomerService:
    return CustomerService(repository)


def get_bank_account_service(
        repository: BankAccountRepository = Depends(get_bank_account_repository),
) -> BankAccountService:
    return BankAccountService(repository)


def get_transaction_service(
        repository: TransactionRepository = Depends(get_transaction_repository),
) -> TransactionService:
    return TransactionService(repository)
