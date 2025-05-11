from pydantic import BaseModel, Field
from typing import Any, Literal, Dict

class WebSocketMessageBase(BaseModel):
    job_id: int
    type: str # Differentiates message types, e.g., 'status', 'partial_result', 'final_result', 'error'
    data: Dict[str, Any] | None = None # Flexible data payload

class WebSocketStatusUpdate(WebSocketMessageBase):
    type: Literal["status_update"] = "status_update"
    status: str # e.g., "PENDING", "PROCESSING_EXPLANATION", "GENERATING_CODE", "COMPLETED", "FAILED"
    message: str | None = None # Optional descriptive message for the status

class WebSocketPartialResult(WebSocketMessageBase):
    type: Literal["partial_result"] = "partial_result"
    result_type: Literal[
        "explanation", 
        "concepts", 
        "storyboard", 
        "enhanced_storyboard", 
        "generated_code", 
        "review_comments"
    ]
    content: str # The actual partial result content

class WebSocketFinalResult(WebSocketMessageBase):
    type: Literal["final_result"] = "final_result"
    refactored_code: str | None = None
    video_url: str | None = None # For Manim video link
    manim_error: str | None = None # For any errors during Manim processing
    message: str = "Processing completed successfully."

class WebSocketError(WebSocketMessageBase):
    type: Literal["error"] = "error"
    error_message: str

# For messages from client to server over WebSocket (if any, besides initial connect)
class WebSocketClientMessage(BaseModel):
    action: str # e.g., 'start_processing', 'subscribe_updates'
    payload: Dict[str, Any] | None = None 