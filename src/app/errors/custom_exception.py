from http import HTTPStatus


class CustomException(Exception):
    code: int
    error_code: int
    error_slug: str
    message: str


class BadRequestException(CustomException):
    code: int = HTTPStatus.BAD_REQUEST
    error_code: int = HTTPStatus.BAD_REQUEST
    error_slug: str = 'BAD_REQUEST'
    message: str = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomException):
    code: int = HTTPStatus.NOT_FOUND
    error_code: int = HTTPStatus.NOT_FOUND
    error_slug: str = 'NOT_FOUND'
    message: str = HTTPStatus.NOT_FOUND.description
