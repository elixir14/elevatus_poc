from bson import ObjectId
from fastapi import status

from elevatus_poc.core import errors
from elevatus_poc.core.database import candidate_collection
from elevatus_poc.core.exceptions import ElevatusHTTPException
from elevatus_poc.core.functions import skip_limit


async def retrieve_candidate(id: str, user_id: str):
    candidate = await candidate_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if not candidate:
        raise ElevatusHTTPException(
            detail="Candidate not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=errors.CANDIDATE_NOT_FOUND
        )
    return candidate


async def retrieve_candidates(user, page_size, page_num, global_search):
    candidates = []
    filters = {"user_id": user.get("id")}
    if global_search:
        filters.update({
            "$or": [
                {"career_level": {"$regex": f"(?i){global_search}(?-i)"}},
                {"job_major": {"$regex": f"(?i){global_search}(?-i)"}},
                {"degree_type": {"$regex": f"(?i){global_search}(?-i)"}},
                {"skills": {"$regex": f"(?i){global_search}(?-i)"}},
            ]
        })
    candidate_instance = candidate_collection.find(filters)
    if page_size:
        skips, limit = skip_limit(page_size=page_size, page_num=page_num)
        candidate_instance = candidate_instance.skip(skips).limit(limit)
    async for candidate in candidate_instance:
        candidates.append(candidate)
    return candidates


async def check_candidate_email_exist(email):
    exist_email = await candidate_collection.find_one({"email": email})
    if exist_email:
        raise ElevatusHTTPException(
            detail="Email already exist",
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=errors.CANDIDATE_EMAIL_ALREADY_EXIST
        )
    return True
