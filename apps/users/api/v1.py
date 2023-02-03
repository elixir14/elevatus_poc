import logging
from datetime import datetime

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from starlette import status

from apps.users.crud import check_user_email_exist
from apps.users.schemas import UserSchema, UserCreateSchema, LoginSchema, TokenBase
from elevatus_poc.core import errors
from elevatus_poc.core.database import user_collection
from elevatus_poc.core.exceptions import ElevatusHTTPException
from elevatus_poc.core.hash import get_password_hash, verify_password

user_router = APIRouter(tags=["User"])
logger = logging.getLogger(__name__)


@user_router.post("/user", response_model=UserSchema)
async def add_user(payload: UserCreateSchema = Body(...)):
    logger.info("User create API called for %s", payload.email)
    user_data = jsonable_encoder(payload)
    await check_user_email_exist(email=user_data.get("email"))
    user_data["created_date"] = datetime.utcnow()
    if user_data.get("password"):
        user_data["password"] = get_password_hash(user_data.get("password"))
    user = await user_collection.insert_one(user_data)
    logger.info("User %s created successfully", payload.email)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return new_user


@user_router.post("/login", response_model=TokenBase)
async def login(payload: LoginSchema, authorize: AuthJWT = Depends()):
    logger.info("Login API called for user: %s", payload.email)
    user = await user_collection.find_one({"email": payload.email})
    if user:
        if verify_password(payload.password, user.get("password")):
            payload = {
                "firstname": user.get("firstname"),
                "lastname": user.get("lastname"),
                "email": user.get("email"),
                "user_type": user.get("user_type"),
            }
            logger.info("Login successfully for user:%s", user.get("email"))
            return {
                "access": authorize.create_access_token(
                    subject=str(user.get("_id")), fresh=True, user_claims=payload
                ),
                "refresh": authorize.create_refresh_token(
                    subject=str(user.get("_id")), user_claims=payload
                ),
            }
    raise ElevatusHTTPException(
        detail="Invalid email or password",
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code=errors.USER_INVALID_EMAIL_OR_PASSWORD
    )
