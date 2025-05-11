# app/main.py
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.backend.config import settings
from app.backend.database import engine, Base
from app.backend.models.agent_job import AgentJob
from app.backend.routes import agent_router
from app.backend.websockets import ws_router
import time

# Create the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for the EdTech platform",
    version=settings.API_VERSION
)

# Print explicitly for debugging
print("\n\n")
print("*" * 80)
print(f"CONFIGURING CORS WITH ORIGINS: {settings.cors_origins_list}")
print("*" * 80)
print("\n\n")

# Configure CORS with explicit options
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including OPTIONS
    allow_headers=["*"],  # Allow all headers including Content-Type
    expose_headers=["*"],
    max_age=86400,  # Cache preflight for a day
)

# Create database tables on startup in development (for simplicity)
# In a production app, you'd use Alembic for migrations instead
@app.on_event("startup")
async def startup_db_client():
    if settings.DEBUG:
        Base.metadata.create_all(bind=engine)
    print("Database initialized")

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Check if the API is running."""
    return {"status": "healthy", "version": settings.API_VERSION}

# CORS test endpoint to verify CORS headers
@app.options("/cors-test")
async def cors_test(request: Request, response: Response):
    origin = request.headers.get("Origin", "")
    print(f"CORS TEST - Received OPTIONS request from: {origin}")
    # CORS headers will be added by middleware
    return {"message": "CORS headers should be present in response"}

# Import and register your routers here
app.include_router(agent_router.router)
app.include_router(ws_router.router)

# Example:
# from app.routes import course_router
# app.include_router(course_router, prefix="/api/courses", tags=["courses"])

# For local development
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)