# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator, validator # validator for older Pydantic if needed
from typing import List, Optional, Any
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
# Remove redundant startup prints from here, main.py will handle them

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables with defaults.
    """
    # Project info
    PROJECT_NAME: str = "EdTech Platform"
    API_PREFIX: str = "/api"  # Added API_PREFIX
    API_VERSION: str = "v1"
    DEBUG: bool = False
    
    # Database connection
    DATABASE_URL: PostgresDsn
    
    # CORS settings
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # Optional: AI API settings
    GEMINI_API_KEY: Optional[str] = None # Renamed from GOOGLE_API_KEY to match common naming

    @property
    def VERSIONED_API_PREFIX(self) -> str:
        """Constructs the versioned API prefix, e.g., /api/v1."""
        return f"{self.API_PREFIX.rstrip('/')}/{self.API_VERSION}"
    
    # Property to access CORS_ORIGINS as a list
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS from string to list when accessed."""
        if not self.CORS_ORIGINS:
            return []
        if self.CORS_ORIGINS.startswith('[') and self.CORS_ORIGINS.endswith(']'):
            try:
                parsed_v = json.loads(self.CORS_ORIGINS)
                if isinstance(parsed_v, list):
                    return [str(origin).strip() for origin in parsed_v if str(origin).strip()]
            except json.JSONDecodeError:
                pass
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',') if origin.strip()]
    
    # Keep validator for CORS_ORIGINS if it serves a purpose for manual instantiation
    # For Pydantic V2, @field_validator is preferred over @validator
    @field_validator("CORS_ORIGINS", mode='before')
    @classmethod
    def parse_cors_origins_input_to_str(cls, v: Any) -> str:
        if isinstance(v, list):
            return ','.join(str(i) for i in v)
        elif isinstance(v, str):
            return v
        elif v is None:
            return ""
        raise TypeError("CORS_ORIGINS must be a string or list of strings")

    # Pydantic V2 style for model configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore' # Allow other env vars without failing
    )

# Create a settings instance for importing in other modules
settings = Settings()

# Centralize startup diagnostic prints in main.py or a dedicated startup log function
# Removing them from here to avoid multiple executions if settings is imported elsewhere.