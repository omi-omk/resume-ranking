from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from bson import ObjectId
import math

from app.core.database import get_database
from app.models.matching import ProcessMatchingRequest, MatchingResponse, MatchingDetailResponse
from app.services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/process")
async def process_matching(request: ProcessMatchingRequest):
    """Process matching for all candidates against a specific job"""
    db = await get_database()
    
    try:
        # Find the job
        job = await db.jobs.find_one({"job_name": request.job_name})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get all candidates
        candidates_cursor = db.candidates.find()
        candidates = await candidates_cursor.to_list(length=None)
        
        processed_count = 0
        skipped_count = 0
        
        for candidate in candidates:
            # Check if matching already exists
            existing_match = await db.matching.find_one({
                "candidate_id": candidate["_id"],
                "job_id": job["_id"]
            })
            
            if existing_match:
                skipped_count += 1
                continue
            
            # Convert ObjectIds to strings for AI processing
            candidate_data = {**candidate}
            candidate_data["_id"] = str(candidate_data["_id"])
            job_data = {**job}
            job_data["_id"] = str(job_data["_id"])
            
            # Analyze matching with AI
            matching_result = await ai_service.analyze_matching(candidate_data, job_data)
            
            # Prepare matching document
            matching_doc = {
                "candidate_id": candidate["_id"],
                "job_id": job["_id"],
                "degree": matching_result["degree"],
                "experience": matching_result["experience"],
                "technical_skill": matching_result["technical_skill"],
                "responsibility": matching_result["responsibility"],
                "certificate": matching_result["certificate"],
                "soft_skill": matching_result["soft_skill"],
                "summary_comment": matching_result["summary_comment"],
                "score": matching_result["score"],
                "created_at": datetime.utcnow()
            }
            
            # Save to database
            await db.matching.insert_one(matching_doc)
            processed_count += 1
        
        return {
            "message": "Matching process completed",
            "processed": processed_count,
            "skipped": skipped_count
        }
        
    except Exception as e:
        logger.error(f"Error processing matching: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process matching")


@router.get("/results")
async def get_matching_results(
    job_name: str = Query(..., description="Job name to filter results"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """Get matching results for a specific job"""
    db = await get_database()
    
    try:
        # Find the job
        job = await db.jobs.find_one({"job_name": job_name})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get all candidates with their matching scores
        candidates_cursor = db.candidates.find()
        candidates = await candidates_cursor.to_list(length=None)
        
        results = []
        for candidate in candidates:
            # Find matching record
            matching = await db.matching.find_one({
                "candidate_id": candidate["_id"],
                "job_id": job["_id"]
            })
            
            result = {
                "id": str(candidate["_id"]),
                "candidate_name": candidate.get("candidate_name", "Unknown"),
                "candidate_email": candidate.get("email", ""),
                "candidate_phone": candidate.get("phone_number", ""),
                "cv_name": candidate.get("cv_name", ""),
                "score": matching["score"] if matching else 0,
                "summary_comment": matching["summary_comment"] if matching else "",
                "matching_status": matching is not None
            }
            results.append(result)
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Paginate results
        total_count = len(results)
        total_pages = math.ceil(total_count / page_size)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_results = results[start_idx:end_idx]
        
        return {
            "results": paginated_results,
            "total_page": total_pages,
            "total_matching": total_count
        }
        
    except Exception as e:
        logger.error(f"Error getting matching results: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get matching results")


@router.get("/detail/{candidate_id}/{job_id}", response_model=MatchingDetailResponse)
async def get_matching_detail(candidate_id: str, job_id: str):
    """Get detailed matching information for a candidate-job pair"""
    db = await get_database()
    
    try:
        # Get candidate
        candidate = await db.candidates.find_one({"_id": ObjectId(candidate_id)})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        # Get job
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get matching record
        matching = await db.matching.find_one({
            "candidate_id": ObjectId(candidate_id),
            "job_id": ObjectId(job_id)
        })
        
        if not matching:
            # Return candidate info without matching details
            return MatchingDetailResponse(
                id=str(candidate["_id"]),
                candidate_name=candidate.get("candidate_name", "Unknown"),
                phone_number=candidate.get("phone_number", ""),
                email=candidate.get("email", ""),
                cv_name=candidate.get("cv_name", ""),
                job_name=job.get("job_name", ""),
                job_recommended=candidate.get("job_recommended", []),
                score=0,
                summary_comment="No matching analysis available",
                degree={"score": 0, "comment": "Not analyzed"},
                experience={"score": 0, "comment": "Not analyzed"},
                technical_skill={"score": 0, "comment": "Not analyzed"},
                responsibility={"score": 0, "comment": "Not analyzed"},
                certificate={"score": 0, "comment": "Not analyzed"},
                soft_skill={"score": 0, "comment": "Not analyzed"}
            )
        
        return MatchingDetailResponse(
            id=str(matching["_id"]),
            candidate_name=candidate.get("candidate_name", "Unknown"),
            phone_number=candidate.get("phone_number", ""),
            email=candidate.get("email", ""),
            cv_name=candidate.get("cv_name", ""),
            job_name=job.get("job_name", ""),
            job_recommended=candidate.get("job_recommended", []),
            score=matching["score"],
            summary_comment=matching["summary_comment"],
            degree=matching["degree"],
            experience=matching["experience"],
            technical_skill=matching["technical_skill"],
            responsibility=matching["responsibility"],
            certificate=matching["certificate"],
            soft_skill=matching["soft_skill"]
        )
        
    except Exception as e:
        logger.error(f"Error getting matching detail: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))