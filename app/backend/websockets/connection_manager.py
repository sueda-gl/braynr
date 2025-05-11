from fastapi import WebSocket
from typing import Dict, List, Any
import json

class ConnectionManager:
    def __init__(self):
        # Stores active connections: job_id -> list of WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, job_id: str, websocket: WebSocket):
        await websocket.accept()
        if job_id not in self.active_connections:
            self.active_connections[job_id] = []
        self.active_connections[job_id].append(websocket)
        print(f"WebSocket connected for job_id {job_id}. Total clients for job: {len(self.active_connections[job_id])}")

    def disconnect(self, job_id: str, websocket: WebSocket):
        if job_id in self.active_connections:
            self.active_connections[job_id].remove(websocket)
            if not self.active_connections[job_id]: # No more clients for this job_id
                del self.active_connections[job_id]
            print(f"WebSocket disconnected for job_id {job_id}. Remaining clients for job: {len(self.active_connections.get(job_id, []))}")
        else:
            print(f"Attempted to disconnect WebSocket for unknown job_id {job_id}")

    async def send_personal_message(self, message: Any, websocket: WebSocket):
        """Sends a message to a specific WebSocket connection."""
        if isinstance(message, dict):
            await websocket.send_json(message)
        else:
            await websocket.send_text(str(message))

    async def broadcast_to_job(self, job_id: str, message: Any):
        """Broadcasts a message to all connected WebSockets for a specific job_id."""
        if job_id in self.active_connections:
            disconnected_clients: List[WebSocket] = []
            for connection in self.active_connections[job_id]:
                try:
                    if isinstance(message, dict):
                        await connection.send_json(message)
                    else:
                        await connection.send_text(str(message))
                except Exception as e:
                    # Handle cases where client might have disconnected abruptly
                    print(f"Error sending message to client for job {job_id}: {e}. Marking for disconnect.")
                    disconnected_clients.append(connection)
            
            # Clean up disconnected clients
            for client in disconnected_clients:
                self.disconnect(job_id, client)
        else:
            print(f"No active connections for job_id {job_id} to broadcast to.")

# Global instance of the ConnectionManager
manager = ConnectionManager() 