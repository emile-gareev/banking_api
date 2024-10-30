from app.db.models import Customer
from app.repositories.base import BasicRepository
from app.routers.internal.v1.schemas import CustomerSchema


class CustomerRepository(BasicRepository):
    """Repository for working with customers."""

    _model = Customer
    _item_schema = CustomerSchema
