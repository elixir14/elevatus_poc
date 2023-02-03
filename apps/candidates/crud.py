from bson import ObjectId
from fastapi import status

from elevatus_poc.core import errors
from elevatus_poc.core.database import candidate_collection
from elevatus_poc.core.exceptions import ElevatusHTTPException


async def retrieve_candidate(id: str, user_id: str):
    candidate = await candidate_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if not candidate:
        raise ElevatusHTTPException(
            detail="Candidate not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=errors.CANDIDATE_NOT_FOUND
        )
    return candidate


async def check_candidate_email_exist(email):
    exist_email = await candidate_collection.find_one({"email": email})
    if exist_email:
        raise ElevatusHTTPException(
            detail="Email already exist",
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=errors.CANDIDATE_EMAIL_ALREADY_EXIST
        )
    return True
