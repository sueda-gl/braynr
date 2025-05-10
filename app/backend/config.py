# app/config.py
from pydantic import BaseSettings, PostgresDsn, validator
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables with defaults.
    """
    # Project info
    PROJECT_NAME: str = "EdTech Platform"
    API_VERSION: str = "v1"
    DEBUG: bool = False
    
    # Database connection
    DATABASE_URL: PostgresDsn
    
    # CORS settings - List of allowed origins
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Optional: AI API settings
    GEMINI_API_KEY: Optional[str] = None
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse the CORS_ORIGINS from a comma-separated string to a list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a settings instance for importing in other modules
settings = Settings()