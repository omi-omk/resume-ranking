from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ScoreComment(BaseModel):
    score: int
    comment: str


class MatchingBase(BaseModel):
    candidate_id: PyObjectId
    job_id: PyObjectId
    degree: ScoreComment
    experience: ScoreComment
    technical_skill: ScoreComment
    responsibility: ScoreComment
    certificate: ScoreComment
    soft_skill: ScoreComment
    summary_comment: str
    score: float


class MatchingCreate(MatchingBase):
    pass


class MatchingInDB(MatchingBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MatchingResponse(MatchingInDB):
    pass


class MatchingDetailResponse(BaseModel):
    id: str
    candidate_name: str
    phone_number: str
    email: str
    cv_name: str
    job_name: str
    job_recommended: list
    score: float
    summary_comment: str
    degree: ScoreComment
    experience: ScoreComment
    technical_skill: ScoreComment
    responsibility: ScoreComment
    certificate: ScoreComment
    soft_skill: ScoreComment


class ProcessMatchingRequest(BaseModel):
    job_name: str