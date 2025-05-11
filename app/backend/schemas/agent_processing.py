from pydantic import BaseModel

class AgentProcessRequest(BaseModel):
    image_data_url: str
    user_prompt: str | None = None

class AgentProcessResponse(BaseModel):
    job_id: int
    status: str
    message: str 

class AgentJobInitResponse(BaseModel):
    job_id: int
    message: str = "Agent job initiated. Connect to WebSocket for updates." 