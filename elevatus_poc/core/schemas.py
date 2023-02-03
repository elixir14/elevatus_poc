from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from elevatus_poc.core.helper import PyObjectId


class ResponseBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_by: Optional[str]
    update_by: Optional[str]
    created_date: Optional[datetime]
    updated_date: Optional[datetime]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
