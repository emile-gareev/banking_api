from fastapi import HTTPException

from app.enums import TransactionTypes


class NotFoundError(HTTPException):
    def __init__(self, message: str = 'Not found') -> None:
        super().__init__(status_code=404, detail={'code': 'NOT_FOUND', 'message': message})


class ItemNotFoundError(HTTPException):
    def __init__(self, item_name, message: str = 'not found') -> None:
        super().__init__(status_code=404, detail={'code': 'NOT_FOUND', 'message': f'{item_name} {message}'})


class NotEnoughEquity(HTTPException):
    def __init__(self, message: str = 'There is not enough equity in the account') -> None:
        super().__init__(status_code=400, detail={'code': 'BAD_REQUEST', 'message': message})


class WrongTransactionType(HTTPException):
    def __init__(
            self,
            message: str = f'You have chosen wrong transaction type. Choose one of {TransactionTypes.as_dict().keys()}',
    ) -> None:
        super().__init__(status_code=400, detail={'code': 'BAD_REQUEST', 'message': message})
