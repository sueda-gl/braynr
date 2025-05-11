from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, Response
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os

from app.backend.database import get_db
from app.backend.models.agent_job import AgentJob
from app.backend.schemas.agent_processing import AgentProcessRequest, AgentJobInitResponse
from app.backend.services.agent_service import process_agent_job
from app.backend.services.ocr_service import extract_text_from_image

router = APIRouter(
    prefix="/api/v1/agent",
    tags=["Agent Processing"]
)

# Add explicit OPTIONS handling for /jobs endpoint to handle CORS preflight
@router.options("/jobs")
async def options_jobs(request: Request, response: Response):
    origin = request.headers.get("Origin", "")
    print(f"OPTIONS request for /api/v1/agent/jobs from origin: {origin}")
    
    # Allow both frontend origins directly (hardcoded approach for troubleshooting)
    allowed_origins = ["http://localhost:5173", "http://localhost:3000"]
    
    # Add CORS headers to response if origin is in allowed list
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        print(f"Added CORS headers for origin: {origin}")
    else:
        print(f"Origin {origin} not in allowed list: {allowed_origins}")
    
    # OPTIONS responses should be empty
    return {}

@router.post("/jobs", response_model=AgentJobInitResponse)
async def create_agent_job(
    request_data: AgentProcessRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    request: Request = None,
    response: Response = None
):
    # Add CORS headers to POST response too (safer approach)
    if request and response:
        origin = request.headers.get("Origin", "")
        # Same hardcoded list as OPTIONS handler
        allowed_origins = ["http://localhost:5173", "http://localhost:3000"] 
        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
    try:
        # 1. Perform OCR
        extracted_text = await extract_text_from_image(request_data.image_data_url)
        user_prompt = request_data.user_prompt
        print(f"--- Agent Router: Received user_prompt in API: '{user_prompt}', extracted_text (first 50 chars): '{extracted_text[:50]}' ---")

        if not extracted_text and extracted_text != "":
            print(f"OCR Service returned no text for image data: {request_data.image_data_url[:100]}...")
            pass

        # 2. Create AgentJob with original image URL and extracted text
        new_job = AgentJob(
            input_image_data_url=request_data.image_data_url,
            input_text=extracted_text,
            status="PENDING"
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)

        # 3. Start agent pipeline with extracted text and user_prompt
        background_tasks.add_task(
            process_agent_job,
            new_job.id,
            extracted_text,
            user_prompt
        )

        return AgentJobInitResponse(job_id=new_job.id)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        print(f"Error in create_agent_job: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create agent job: {str(e)}")

# Note on passing DB session to background tasks is now handled:
# process_agent_job in agent_service.py creates its own SessionLocal(). 