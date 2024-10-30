from fastapi import HTTPException, status


class UnauthorizedHTTPException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect username or password'
    headers = None

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class BasicAuthUnauthorizedHTTPException(UnauthorizedHTTPException):
    headers = {'WWW-Authenticate': 'Basic'}
