from enum import Enum


class TransactionTypes(Enum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'

    @classmethod
    def as_dict(cls):
        return {elm.name: elm.value for elm in cls}
