from sqlalchemy.orm import Session
from app.backend.database import SessionLocal # For creating new sessions in background tasks
from app.backend.models.agent_job import AgentJob
from app.backend.services.root_agent.agent import root_agent # The actual agent
from app.backend.websockets.connection_manager import manager
from app.backend.schemas.websocket_messages import (
    WebSocketStatusUpdate,
    WebSocketPartialResult,
    WebSocketFinalResult,
    WebSocketError
)
import traceback # For logging full error trace
import re # For extracting placeholders from instruction templates

# Import Google ADK dependencies
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Define status constants for clarity
JOB_STATUS_PROCESSING = "PROCESSING"
JOB_STATUS_COMPLETED = "COMPLETED"
JOB_STATUS_FAILED = "FAILED"

# Define detailed status messages for different agent stages
AGENT_STAGES = {
    "ClearExplanationAgent": "Generating clear explanation...",
    "ConceptSeparatorAgent": "Separating concepts...",
    "StoryboardCreatorAgent": "Creating storyboard...",
    "StoryboardEnhancerAgent": "Enhancing storyboard...",
    "CodeGeneratorAgent": "Generating Manim code...",
    "CodeReviewerAgent": "Reviewing code...",
    "CodeRefactorerAgent": "Refactoring code..."
}

# Constants for ADK integration
APP_NAME = "braynr-app"

async def update_job_status_and_broadcast(db: Session, job_id: int, job_id_str: str, status: str, message: str = None, data_to_save: dict = None):
    """Helper to update job status in DB and broadcast to WebSocket."""
    job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
    if job:
        job.status = status
        if data_to_save:
            for key, value in data_to_save.items():
                if hasattr(job, key):
                    setattr(job, key, value)
        db.commit()
        ws_message = WebSocketStatusUpdate(
            job_id=job_id,
            status=status,
            message=message or status # Use status as message if no specific message
        ).model_dump()
        await manager.broadcast_to_job(job_id_str, ws_message)
    else:
        print(f"Job {job_id} not found for status update.")


async def send_partial_result_and_save(db: Session, job_id: int, job_id_str: str, result_type: str, content: str, db_field: str):
    """Helper to send partial result via WebSocket and save to DB."""
    job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
    if job:
        if hasattr(job, db_field):
            setattr(job, db_field, content)
            db.commit()
        
        ws_message = WebSocketPartialResult(
            job_id=job_id,
            result_type=result_type,
            content=content
        ).model_dump()
        await manager.broadcast_to_job(job_id_str, ws_message)
    else:
        print(f"Job {job_id} not found for sending partial result.")


def extract_placeholders(instruction: str) -> list:
    """Extract placeholders from an instruction template string."""
    if not instruction:
        return []
    # Find all {placeholder} patterns in the instruction
    placeholders = re.findall(r'{([^{}]*)}', instruction)
    return list(set(placeholders))  # Remove duplicates


async def process_agent_job(job_id: int, input_text: str, user_prompt: str | None = None):
    """
    Process an agent job using Google ADK infrastructure.
    This function correctly initializes ADK session management and runners.
    """
    print(f"--- Agent Service: process_agent_job received job_id: {job_id}, input_text (first 50): '{input_text[:50]}...', user_prompt: '{user_prompt}' ---")
    job_id_str = str(job_id) # For WebSocket manager
    db: Session = SessionLocal() # Create a new session for this background task
    
    # Create session service for ADK
    session_service = InMemorySessionService()
    
    try:
        await update_job_status_and_broadcast(db, job_id, job_id_str, JOB_STATUS_PROCESSING, "Initializing agent pipeline...")

        # Initial state for the session
        initial_state = {
            "topic": input_text,
            "user_prompt": user_prompt if user_prompt is not None else "" # Ensure user_prompt is always present
        }
        print(f"--- Agent Service: Initial agent state for job {job_id}: {initial_state} ---")

        # Create ADK session with initial state
        session = session_service.create_session(
            app_name=APP_NAME,
            user_id=str(job_id),  # Use job_id as user_id to keep sessions separate
            session_id="session-1",  # Fixed session_id for simplicity
            state=initial_state
        )

        # Create a runner for the agent
        runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )

        # Track which agents have been processed
        processed_agents = set()
        
        # Create a simple user input message to start the agent
        user_message = types.Content(
            role="user",
            parts=[types.Part(text=f"Process this image with text: {input_text}. User prompt: {user_prompt or ''}")]
        )
        
        # Run the agent pipeline and process events
        try:
            for event in runner.run(
                user_id=str(job_id),
                session_id="session-1",
                new_message=user_message
            ):
                # Process events from agents (could be text outputs, thoughts, etc.)
                if hasattr(event, 'author') and event.author not in processed_agents:
                    # A new agent is being processed
                    agent_name = event.author
                    processed_agents.add(agent_name)
                    
                    # Update status for this agent if we have a predefined stage message
                    if agent_name in AGENT_STAGES:
                        await update_job_status_and_broadcast(
                            db, job_id, job_id_str, 
                            JOB_STATUS_PROCESSING, 
                            AGENT_STAGES[agent_name]
                        )
                        print(f"Job {job_id}: Processing agent: {agent_name}")

            # After all agents processed, get the final state
            final_session = session_service.get_session(
                app_name=APP_NAME,
                user_id=str(job_id),
                session_id="session-1"
            )
            
            # Extract results from final state
            final_state = final_session.state
            print(f"Job {job_id}: Final state keys: {list(final_state.keys())}")
            
            # Map output keys to database fields
            db_field_map = {
                'explanation': 'explanation',
                'concepts': 'concepts',
                'storyboard': 'storyboard',
                'enhanced_storyboard': 'enhanced_storyboard',
                'generated_code': 'generated_code',
                'review_comments': 'review_comments',
                'refactored_code': 'refactored_code'
            }
            
            # Send partial results for each output
            for key, db_field in db_field_map.items():
                if key in final_state and key != 'refactored_code': # Exclude refactored_code from partial results
                    content = str(final_state[key])
                    await send_partial_result_and_save(db, job_id, job_id_str, key, content, db_field)
            
            # Get the final code (or empty string if not available)
            final_code = final_state.get('refactored_code', 'No refactored code produced.')
            
            # Update job status to completed
            await update_job_status_and_broadcast(
                db, job_id, job_id_str, 
                JOB_STATUS_COMPLETED, 
                "Agent pipeline completed.", 
                data_to_save={'refactored_code': final_code}
            )
            
            # Send final result
            ws_final_msg = WebSocketFinalResult(job_id=job_id, refactored_code=final_code).model_dump()
            await manager.broadcast_to_job(job_id_str, ws_final_msg)
            
        except Exception as agent_exc:
            error_message = f"Error in agent execution: {str(agent_exc)}"
            print(f"Job {job_id}: {error_message}")
            print(traceback.format_exc())
            
            job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
            if job: 
                job.error_message = error_message
                db.commit()
                
            await update_job_status_and_broadcast(
                db, job_id, job_id_str, 
                JOB_STATUS_FAILED, 
                error_message, 
                data_to_save={'error_message': error_message}
            )
            
            # Send specific error over WebSocket
            ws_err_msg = WebSocketError(job_id=job_id, error_message=error_message).model_dump()
            await manager.broadcast_to_job(job_id_str, ws_err_msg)
            return # Stop processing this job

    except Exception as e:
        error_message = f"Unhandled error in agent processing job {job_id}: {str(e)}"
        print(error_message)
        print(traceback.format_exc())
        
        job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
        # Ensure job status is FAILED and error message is saved
        if job:
            job.status = JOB_STATUS_FAILED
            job.error_message = job.error_message + " | " + error_message if job.error_message else error_message
            db.commit()

        # Broadcast generic failure status and specific error message
        ws_status_fail_msg = WebSocketStatusUpdate(job_id=job_id, status=JOB_STATUS_FAILED, message="Pipeline failed unexpectedly.").model_dump()
        await manager.broadcast_to_job(job_id_str, ws_status_fail_msg)
        ws_err_msg = WebSocketError(job_id=job_id, error_message=error_message).model_dump()
        await manager.broadcast_to_job(job_id_str, ws_err_msg)
    finally:
        db.close() # Ensure session is closed 