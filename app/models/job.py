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


class JobBase(BaseModel):
    job_name: str
    job_description: str
    degree: List[str] = []
    experience: List[str] = []
    technical_skill: List[str] = []
    responsibility: List[str] = []
    certificate: List[str] = []
    soft_skill: List[str] = []


class JobCreate(BaseModel):
    job_name: str
    job_description: str


class JobUpdate(BaseModel):
    job_name: Optional[str] = None
    job_description: Optional[str] = None


class JobInDB(JobBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class JobResponse(JobInDB):
    pass


class JobListResponse(BaseModel):
    results: List[JobResponse]
    total_page: int
    total_job: int