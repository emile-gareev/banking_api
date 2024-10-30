from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.mixin import TimeMixin
from app.db.models.base import Base


class Customer(Base, TimeMixin):
    __tablename__ = 'customers'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)  # noqa
    name = Column(String(100))


class BankAccount(Base, TimeMixin):
    __tablename__ = 'bank_accounts'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)  # noqa
    customer_id = Column(Integer, ForeignKey('customers.id'))
    balance = Column(Float, default=0)

    customer = relationship('Customer', backref='accounts', foreign_keys=[customer_id])
    # transactions = relationship('Transaction', backref='account')


class Transaction(Base, TimeMixin):
    __tablename__ = 'transactions'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)  # noqa
    from_bank_account_id = Column(Integer, ForeignKey('bank_accounts.id'), nullable=True)
    to_bank_account_id = Column(Integer, ForeignKey('bank_accounts.id'), nullable=True)
    amount = Column(Float)
    type = Column(String(32))  # noqa

    from_bank_account = relationship('BankAccount', backref='outgoing_transactions', foreign_keys=[to_bank_account_id])
    to_bank_account = relationship('BankAccount', backref='incoming_transactions', foreign_keys=[from_bank_account_id])
