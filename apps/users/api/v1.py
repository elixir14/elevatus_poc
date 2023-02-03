from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from apps.users.schemas import UserSchema, UserCreateSchema
from elevatus_poc.core.database import user_collection
from elevatus_poc.core.hash import get_password_hash

user_router = APIRouter()


# TODO: limit to only one with same email
@user_router.post("/", response_description="User data added to DB", response_model=UserSchema)
async def add_user_data(user: UserCreateSchema = Body(...)):
    user_data = jsonable_encoder(user)

    if user_data.get("password"):
        user_data["password"] = get_password_hash(user_data.get("password"))
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return new_user
