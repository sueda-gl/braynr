# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.backend.config import settings
from app.backend.database import engine, Base

# Create the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for the EdTech platform",
    version=settings.API_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# TODO: Import and register your routers here
# Example:
# from app.routes import course_router
# app.include_router(course_router, prefix="/api/courses", tags=["courses"])

# For local development
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)