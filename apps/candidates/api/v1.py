import logging
from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from apps.candidates.crud import retrieve_candidate, check_candidate_email_exist
from apps.candidates.schemas import (
    CandidateCreateSchema, CandidateSchema, CandidateUpdateSchema
)
from elevatus_poc.core.database import candidate_collection
from elevatus_poc.core.functions import skip_limit
from elevatus_poc.core.hash import get_password_hash
from elevatus_poc.core.permissions import valid_user

candidate_router = APIRouter(prefix="/candidate", tags=["Candidate"])
logger = logging.getLogger(__name__)


@candidate_router.get("/all", response_model=List[CandidateSchema])
async def get_candidates(
        page_size: int = 10,
        page_num: int = 1,
        user: dict = Depends(valid_user)):
    logger.info("Candidate get API called for %s", user.get("email"))
    candidates = []
    skips, limit = skip_limit(page_size=page_size, page_num=page_num)
    candidate_instance = candidate_collection.find(
        {"user_id": user.get("id")}
    ).skip(skips).limit(limit)
    async for candidate in candidate_instance:
        candidates.append(candidate)
    logger.info("Candidates fetched successfully for user: %s", user.get("email"))
    return candidates


@candidate_router.post("/", response_model=CandidateSchema)
async def add_candidate(
        payload: CandidateCreateSchema = Body(...),
        user: dict = Depends(valid_user)
):
    logger.info("Candidate create API called for %s", user.get("email"))
    candidate_data = jsonable_encoder(payload)
    await check_candidate_email_exist(email=candidate_data.get("email"))
    candidate_data["created_date"] = datetime.utcnow()
    candidate_data["user_id"] = user.get("id")
    if candidate_data.get("password"):
        candidate_data["password"] = get_password_hash(candidate_data.get("password"))
    candidate = await candidate_collection.insert_one(candidate_data)
    new_user = await candidate_collection.find_one({"_id": candidate.inserted_id})
    logger.info(
        "Candidate %s created successfully for user: %s", new_user.get("email"),
        user.get("email")
    )
    return new_user


@candidate_router.get("/{id}", response_model=CandidateSchema)
async def get_candidate_data(id: str, user: dict = Depends(valid_user)):
    logger.info("Candidate detail API called for %s", user.get("email"))
    candidate = await retrieve_candidate(id, user.get("id"))
    logger.info("Candidate %s fetched successfully for user: %s", id, user.get("email"))
    return candidate


@candidate_router.put("/{id}", response_model=CandidateSchema)
async def update_candidate_data(
        id: str,
        payload: CandidateUpdateSchema = Body(...),
        user: dict = Depends(valid_user)
):
    logger.info("Candidate update API called for %s", user.get("email"))
    candidate_data = {k: v for k, v in payload.dict().items() if v is not None}
    candidate_data["updated_date"] = datetime.utcnow()
    if len(candidate_data) < 1:
        return False
    candidate = await retrieve_candidate(id, user.get("id"))
    if candidate:
        await candidate_collection.update_one({"_id": ObjectId(id)}, {"$set": candidate_data})
    logger.info("Candidate %s updated successfully for user: %s", id, user.get("email"))
    return candidate


@candidate_router.delete("/{id}")
async def delete_candidate_data(id: str, user: dict = Depends(valid_user)):
    logger.info("Candidate delete API called for %s", user.get("email"))
    candidate = await retrieve_candidate(id, user.get("id"))
    if candidate:
        await candidate_collection.delete_one({"_id": ObjectId(id)})
    logger.info("Candidate %s deleted successfully for user: %s", id, user.get("email"))
    return "Candidate deleted success"
