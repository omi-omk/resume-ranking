from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List
from datetime import datetime
from bson import ObjectId
import math

from app.core.database import get_database
from app.models.candidate import CandidateResponse, CandidateListResponse, CandidateUpdate
from app.services.ai_service import ai_service
from app.services.document_service import document_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=dict)
async def upload_candidates(files: List[UploadFile] = File(...)):
    """Upload and analyze candidate CV files"""
    db = await get_database()
    results = []
    
    for file in files:
        try:
            # Validate file type
            if not document_service.is_allowed_file(file.filename):
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": "Invalid file type. Only PDF and DOCX are allowed."
                })
                continue
            
            # Save file and get hash
            filename, file_hash = await document_service.save_uploaded_file(file)
            
            # Check if file already exists
            existing = await db.candidates.find_one({"filehash": file_hash})
            if existing:
                results.append({
                    "filename": file.filename,
                    "status": "skipped",
                    "message": "File already exists"
                })
                continue
            
            # Extract text content
            cv_content = document_service.extract_text_from_file(filename)
            if not cv_content:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": "Could not extract text from file"
                })
                continue
            
            # Analyze with AI
            analysis_result = await ai_service.analyze_candidate(cv_content)
            
            # Prepare candidate data
            candidate_data = {
                **analysis_result,
                "cv_name": file.filename,
                "filehash": file_hash,
                "created_at": datetime.utcnow()
            }
            
            # Save to database
            result = await db.candidates.insert_one(candidate_data)
            
            results.append({
                "filename": file.filename,
                "status": "success",
                "candidate_id": str(result.inserted_id)
            })
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": str(e)
            })
    
    return {"results": results}


@router.get("/", response_model=CandidateListResponse)
async def list_candidates(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """Get paginated list of candidates"""
    db = await get_database()
    
    # Count total documents
    total_count = await db.candidates.count_documents({})
    total_pages = math.ceil(total_count / page_size)
    
    # Get paginated results
    skip = (page - 1) * page_size
    cursor = db.candidates.find().skip(skip).limit(page_size).sort("created_at", -1)
    candidates = await cursor.to_list(length=page_size)
    
    # Convert ObjectId to string
    for candidate in candidates:
        candidate["_id"] = str(candidate["_id"])
    
    return CandidateListResponse(
        results=candidates,
        total_page=total_pages,
        total_file=total_count
    )


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: str):
    """Get candidate by ID"""
    db = await get_database()
    
    try:
        candidate = await db.candidates.find_one({"_id": ObjectId(candidate_id)})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        candidate["_id"] = str(candidate["_id"])
        return candidate
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid candidate ID")


@router.put("/{candidate_id}")
async def update_candidate(candidate_id: str, candidate_update: CandidateUpdate):
    """Update candidate information"""
    db = await get_database()
    
    try:
        # Prepare update data
        update_data = {k: v for k, v in candidate_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No data to update")
        
        result = await db.candidates.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        return {"message": "Candidate updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{candidate_id}")
async def delete_candidate(candidate_id: str):
    """Delete candidate"""
    db = await get_database()
    
    try:
        # Get candidate to delete associated file
        candidate = await db.candidates.find_one({"_id": ObjectId(candidate_id)})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        # Delete from database
        await db.candidates.delete_one({"_id": ObjectId(candidate_id)})
        
        # Delete associated matching records
        await db.matching.delete_many({"candidate_id": ObjectId(candidate_id)})
        
        # Delete file
        if "cv_name" in candidate:
            await document_service.delete_file(candidate["cv_name"])
        
        return {"message": "Candidate deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))