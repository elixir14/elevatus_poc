from bson import ObjectId
from fastapi import status

from elevatus_poc.core import errors
from elevatus_poc.core.database import user_collection
from elevatus_poc.core.exceptions import ElevatusHTTPException


async def retrieve_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if not user:
        raise ElevatusHTTPException(
            detail="User not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=errors.USER_NOT_FOUND
        )
    return user


async def check_user_email_exist(email):
    exist_email = await user_collection.find_one({"email": email})
    if exist_email:
        raise ElevatusHTTPException(
            detail="Email already exist",
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=errors.USER_EMAIL_ALREADY_EXIST
        )
    return True
