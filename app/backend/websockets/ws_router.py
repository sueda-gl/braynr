from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Path, Depends
from sqlalchemy.orm import Session
import json # For serializing Pydantic models to JSON strings for WebSocket

from app.backend.database import get_db
from app.backend.models.agent_job import AgentJob
from app.backend.websockets.connection_manager import manager
from app.backend.schemas.websocket_messages import WebSocketError 

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket Agent Updates"]
)

@router.websocket("/agent_updates/{job_id_str}") # Renamed job_id to job_id_str for clarity
async def websocket_endpoint(
    websocket: WebSocket, 
    job_id_str: str = Path(..., title="The ID of the agent job to subscribe to"),
    db: Session = Depends(get_db) 
):
    try:
        job_id = int(job_id_str) # Convert path parameter to int
    except ValueError:
        await websocket.accept()
        error_payload = WebSocketError(job_id=-1, type='error', error_message=f"Invalid job_id format: {job_id_str}. Must be an integer.").model_dump()
        await websocket.send_json(error_payload)
        await websocket.close(code=1008) # Policy Violation
        print(f"WebSocket connection rejected for invalid job_id format: {job_id_str}")
        return

    job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
    if not job:
        await websocket.accept() 
        error_payload = WebSocketError(job_id=job_id, type='error', error_message=f"Job with ID {job_id} not found.").model_dump()
        await websocket.send_json(error_payload)
        await websocket.close(code=1008) 
        print(f"WebSocket connection rejected for non-existent job_id: {job_id}")
        return

    await manager.connect(job_id_str, websocket) # Use original job_id_str for manager key if preferred
    try:
        # Connection established, inform client (optional)
        # await manager.send_personal_message({"type": "connection_ack", "job_id": job_id, "message": "Connected for updates."}, websocket)
        
        while True:
            # This loop keeps the connection alive.
            # We are primarily using this for server-to-client communication via manager.broadcast_to_job().
            # If client needs to send messages, it would be `data = await websocket.receive_text()` or `receive_json()`
            # For now, if client sends anything, we'll just effectively ignore it and keep listening.
            # A robust implementation might handle specific client messages or use a timeout.
            await websocket.receive_text() # Keeps the connection open. Will raise WebSocketDisconnect if client closes.
            # If we wanted to process client messages: 
            # data = await websocket.receive_text()
            # print(f"Received from client for job {job_id_str}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(job_id_str, websocket)
        print(f"Client for job_id {job_id_str} disconnected.")
    except Exception as e:
        # Attempt to gracefully close on other errors
        manager.disconnect(job_id_str, websocket)
        print(f"Exception in WebSocket for job_id {job_id_str}: {type(e).__name__} - {e}")
        try:
            await websocket.close(code=1011) # Internal Server Error
        except RuntimeError: # Websocket might already be closed
            pass 