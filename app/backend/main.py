# app/main.py
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.backend.config import settings
from app.backend.database import engine, Base
from app.backend.models import agent_job
from app.backend.routes import agent_router
from app.backend.websockets import ws_router
import time
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

# Create the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for the EdTech platform",
    version=settings.API_VERSION,
    openapi_url=f"{settings.VERSIONED_API_PREFIX}/openapi.json"
)

# Ensure static content directory exists
# Path should be relative to the location of main.py or an absolute path
# Assuming main.py is in app/backend/
STATIC_MANIM_DIR = Path(__file__).parent / "static_content" / "manim_videos"
STATIC_MANIM_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files directory for serving Manim videos
# The URL path "/static_manim" will serve files from STATIC_MANIM_DIR
app.mount("/static_manim", StaticFiles(directory=STATIC_MANIM_DIR), name="static_manim_videos")

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
async def on_startup():
    print("********************************************************************************")
    print("LOADING CONFIG AND ENV VARIABLES (from main.py on_startup)")
    print("********************************************************************************")
    print(f"CORS SETTINGS RAW: {settings.CORS_ORIGINS}")
    print(f"CORS ORIGINS LIST: {settings.cors_origins_list}")
    print(f"Using database URL: {settings.DATABASE_URL.get_secret_value() if hasattr(settings.DATABASE_URL, 'get_secret_value') else str(settings.DATABASE_URL)}")
    print(f"API Prefix: {settings.API_PREFIX}")
    print(f"API Version: {settings.API_VERSION}")
    print(f"Versioned API Prefix: {settings.VERSIONED_API_PREFIX}")
    print(f"Debug Mode: {settings.DEBUG}")
    print("********************************************************************************")
    if settings.DEBUG:
        Base.metadata.create_all(bind=engine)
        print("Database tables created (DEBUG mode).")
    else:
        print("Database tables NOT created (production mode - use migrations).")
    print("Application startup complete.")

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
app.include_router(
    agent_router.router, 
    prefix=f"{settings.VERSIONED_API_PREFIX}/agent",  # This makes paths like /api/v1/agent/jobs
    tags=["agent"]
)
app.include_router(
    ws_router.router, 
    prefix=settings.VERSIONED_API_PREFIX, # Assuming ws_router defines paths like /ws/agent_updates/...
    tags=["websockets"]
)

# Example:
# from app.routes import course_router
# app.include_router(course_router, prefix="/api/courses", tags=["courses"])

# Main root path, not versioned
@app.get("/", tags=["root"])
async def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

# For local development
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)