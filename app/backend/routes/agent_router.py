from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, Response
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os

from app.backend.database import get_db
from app.backend.models.agent_job import AgentJob
from app.backend.schemas.agent_processing import AgentProcessRequest, AgentJobInitResponse
from app.backend.services.agent_service import process_agent_job
from app.backend.services.ocr_service import extract_text_from_image

# Remove the prefix from APIRouter; it will be handled by main.py
router = APIRouter(
    # prefix="/api/v1/agent", # REMOVED
    tags=["Agent Processing"] # Tags are still useful
)

# Add explicit OPTIONS handling for /jobs endpoint to handle CORS preflight
@router.options("/jobs")
async def options_jobs(request: Request, response: Response):
    origin = request.headers.get("Origin", "")
    print(f"OPTIONS request for /jobs from origin: {origin} (router path, before main prefix)")
    
    # Allow both frontend origins directly (hardcoded approach for troubleshooting)
    # This CORS handling might be better managed globally by the middleware in main.py
    allowed_origins = ["http://localhost:5173", "http://localhost:3000"]
    
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        print(f"Added CORS headers for origin: {origin} directly in /jobs OPTIONS handler")
    else:
        print(f"Origin {origin} not in allowed list for /jobs OPTIONS: {allowed_origins}")
    
    return {}

@router.post("/jobs", response_model=AgentJobInitResponse)
async def create_agent_job(
    request_data: AgentProcessRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    request: Request = None, # Make request and response optional or ensure they are always passed
    response: Response = None
):
    # This local CORS header setting might conflict or be redundant with global middleware.
    # It's generally better to handle CORS globally in main.py.
    if request and response:
        origin = request.headers.get("Origin", "")
        allowed_origins = ["http://localhost:5173", "http://localhost:3000"] 
        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            print(f"Added CORS headers for origin: {origin} directly in /jobs POST handler")
        
    try:
        # 1. Perform OCR
        extracted_text = await extract_text_from_image(request_data.image_data_url)
        user_prompt = request_data.user_prompt
        print(f"--- Agent Router (/jobs): Received user_prompt: '{user_prompt}', extracted_text (first 50): '{extracted_text[:50]}' ---")

        if not extracted_text and extracted_text != "":
            print(f"OCR Service returned no text for image data: {request_data.image_data_url[:100]}...")
            pass # Allow processing even if OCR fails for now

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
        print(f"HTTPException in create_agent_job: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        db.rollback()
        print(f"Error in create_agent_job (/jobs): {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create agent job: {str(e)}")

# Note on passing DB session to background tasks is now handled:
# process_agent_job in agent_service.py creates its own SessionLocal(). 