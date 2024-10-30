from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional

from app.dependencies.repository import get_user_repository
from app.errors.security import BasicAuthUnauthorizedHTTPException
from app.repositories.security import UserRepository, UserSchema
from app.utils.security import validate_password

security = HTTPBasic()


async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    repository: UserRepository = Depends(get_user_repository),
) -> Optional[UserSchema]:
    """Authorize the current user from the request."""

    current_username, current_password = credentials.username, credentials.password
    current_user = await repository.get_user_by_username(current_username)
    if not (current_user and validate_password(current_password, current_user.password)):
        raise BasicAuthUnauthorizedHTTPException

    return current_user
