from pydantic import BaseModel, Field
from typing import List, Optional
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


class CandidateBase(BaseModel):
    candidate_name: str
    phone_number: str
    email: str
    comment: str
    degree: List[str] = []
    experience: List[str] = []
    technical_skill: List[str] = []
    responsibility: List[str] = []
    certificate: List[str] = []
    soft_skill: List[str] = []
    job_recommended: List[str] = []
    office: int = 0
    sql: int = 0


class CandidateCreate(CandidateBase):
    cv_name: str
    filehash: str


class CandidateUpdate(BaseModel):
    candidate_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    comment: Optional[str] = None


class CandidateInDB(CandidateBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cv_name: str
    filehash: str
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CandidateResponse(CandidateInDB):
    pass


class CandidateListResponse(BaseModel):
    results: List[CandidateResponse]
    total_page: int
    total_file: int