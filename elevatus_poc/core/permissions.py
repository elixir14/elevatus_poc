import logging

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from starlette import status

from elevatus_poc.core import errors
from elevatus_poc.core.exceptions import ElevatusHTTPException

logger = logging.getLogger(__name__)


def valid_user(authorize: AuthJWT = Depends()):
    try:
        logger.debug('Valid User')
        authorize.jwt_required()
    except Exception as err:
        raise ElevatusHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            error_code=errors.AUTH_TOKEN_INVALID
        )
    user = authorize.get_raw_jwt()
    user["id"] = authorize.get_jwt_subject()
    return user
