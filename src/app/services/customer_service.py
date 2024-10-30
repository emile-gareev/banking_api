from logging import getLogger

from app.repositories import CustomerRepository
from app.services.base_service import BaseService

logger = getLogger(__file__)


class CustomerService(BaseService):
    """Service for work with customers."""

    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository
