from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from bson import ObjectId
import math

from app.core.database import get_database
from app.models.job import JobCreate, JobUpdate, JobResponse, JobListResponse
from app.services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=JobResponse)
async def create_job(job_data: JobCreate):
    """Create a new job"""
    db = await get_database()
    
    try:
        # Analyze job description with AI
        analysis_result = await ai_service.analyze_job(job_data.job_description)
        
        # Prepare job data
        job_doc = {
            "job_name": job_data.job_name.strip(),
            "job_description": job_data.job_description.strip(),
            **analysis_result,
            "created_at": datetime.utcnow()
        }
        
        # Save to database
        result = await db.jobs.insert_one(job_doc)
        
        # Return created job
        job_doc["_id"] = str(result.inserted_id)
        return job_doc
        
    except Exception as e:
        logger.error(f"Error creating job: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create job")


@router.get("/", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """Get paginated list of jobs"""
    db = await get_database()
    
    # Count total documents
    total_count = await db.jobs.count_documents({})
    total_pages = math.ceil(total_count / page_size)
    
    # Get paginated results
    skip = (page - 1) * page_size
    cursor = db.jobs.find().skip(skip).limit(page_size).sort("created_at", -1)
    jobs = await cursor.to_list(length=page_size)
    
    # Convert ObjectId to string
    for job in jobs:
        job["_id"] = str(job["_id"])
    
    return JobListResponse(
        results=jobs,
        total_page=total_pages,
        total_job=total_count
    )


@router.get("/all", response_model=List[JobResponse])
async def get_all_jobs():
    """Get all jobs (for dropdown selections)"""
    db = await get_database()
    
    cursor = db.jobs.find().sort("job_name", 1)
    jobs = await cursor.to_list(length=None)
    
    # Convert ObjectId to string
    for job in jobs:
        job["_id"] = str(job["_id"])
    
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """Get job by ID"""
    db = await get_database()
    
    try:
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job["_id"] = str(job["_id"])
        return job
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid job ID")


@router.put("/{job_id}")
async def update_job(job_id: str, job_update: JobUpdate):
    """Update job"""
    db = await get_database()
    
    try:
        # Get existing job
        existing_job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not existing_job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Prepare update data
        update_data = {k: v for k, v in job_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No data to update")
        
        # If job description changed, re-analyze
        if "job_description" in update_data:
            analysis_result = await ai_service.analyze_job(update_data["job_description"])
            update_data.update(analysis_result)
        
        # Update job
        result = await db.jobs.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": update_data}
        )
        
        return {"message": "Job updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """Delete job"""
    db = await get_database()
    
    try:
        # Delete job
        result = await db.jobs.delete_one({"_id": ObjectId(job_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Delete associated matching records
        await db.matching.delete_many({"job_id": ObjectId(job_id)})
        
        return {"message": "Job deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))