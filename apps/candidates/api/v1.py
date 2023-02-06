import logging
import os
import tempfile

import numpy as np
import pandas as pd
from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import FileResponse

from apps.candidates.crud import (
    retrieve_candidate, check_candidate_email_exist, retrieve_candidates)
from apps.candidates.schemas import (
    CandidateCreateSchema, CandidateSchema, CandidateUpdateSchema
)
from elevatus_poc.core.database import candidate_collection
from elevatus_poc.core.permissions import valid_user

candidate_router = APIRouter(prefix="/candidate", tags=["Candidate"])
logger = logging.getLogger(__name__)


@candidate_router.get("/all", response_model=List[CandidateSchema])
async def get_candidates(
        page_size: int = Query(""),
        page_num: int = 1,
        global_search: str = Query(""),
        user: dict = Depends(valid_user)):
    logger.info("Candidate get API called for %s", user.get("email"))
    candidates = await retrieve_candidates(user, page_size, page_num, global_search)
    logger.info("Candidates fetched successfully for user: %s", user.get("email"))
    return candidates


@candidate_router.get("/generate-report")
async def get_candidates_report(
        page_size: int = Query(""),
        page_num: int = 1,
        global_search: str = Query(""),
        user: dict = Depends(valid_user)):
    logger.info("Candidate report generate API called for %s", user.get("email"))
    candidates = await retrieve_candidates(user, page_size, page_num, global_search)
    with tempfile.NamedTemporaryFile(delete=False) as file:
        dataframe = pd.DataFrame(candidates)
        dataframe = dataframe.drop(columns=["_id"])
        dataframe.index = np.arange(1, len(dataframe) + 1)
        dataframe.index.names = ['#']
        file_name = os.path.join(tempfile.tempdir, file.name)
        dataframe.to_csv(file_name)
        headers = {
            'Content-Disposition': f'attachment; filename="Candidates.csv"',
            'Access-Control-Expose-Headers': 'Content-Disposition'
        }
        logger.info("Candidates report generated successfully for user: %s", user.get("email"))
        return FileResponse(
            file_name, media_type='application/octet-stream', headers=headers
        )


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
