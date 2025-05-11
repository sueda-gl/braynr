# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator
from typing import List, Optional, Any
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
print("\n\n")
print("*" * 80)
print("LOADING CONFIG AND ENV VARIABLES")
print("*" * 80)
print("\n\n")

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
    
    # CORS settings - Changed to str to avoid automatic JSON parsing
    # HARD-CODED BOTH LOCALHOST ORIGINS FOR TESTING
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"  # Added 5173 explicitly
    
    # Optional: AI API settings
    GEMINI_API_KEY: Optional[str] = None
    
    # Property to access CORS_ORIGINS as a list
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS from string to list when accessed."""
        if not self.CORS_ORIGINS:
            return []
            
        # Try JSON parsing first if it looks like JSON
        if self.CORS_ORIGINS.startswith('[') and self.CORS_ORIGINS.endswith(']'):
            try:
                parsed_v = json.loads(self.CORS_ORIGINS)
                if isinstance(parsed_v, list):
                    return [str(origin).strip() for origin in parsed_v if str(origin).strip()]
            except json.JSONDecodeError:
                # Not valid JSON, fall through to comma-separated parsing
                pass
                
        # Parse as comma-separated
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',') if origin.strip()]
    
    @field_validator("CORS_ORIGINS", mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Any) -> str:
        """Validate CORS_ORIGINS input - only for direct setting in code, not env vars."""
        if isinstance(v, list):
            # Convert list back to comma-separated string
            return ','.join(str(i) for i in v)
        elif isinstance(v, str):
            return v
        elif v is None:
            return ""
        raise TypeError("CORS_ORIGINS must be a string or list")
    
    # Pydantic V2 style for model configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'
    )

# Create a settings instance for importing in other modules
settings = Settings()

print("\n\n")
print("*" * 80)
print(f"CORS SETTINGS: RAW={settings.CORS_ORIGINS}")
print(f"CORS ORIGINS LIST: {settings.cors_origins_list}")
print("*" * 80)
print("\n\n")

# IMPORTANT: Update FastAPI CORS middleware to use the parsed list property
# Whenever you use settings.CORS_ORIGINS in FastAPI's CORS middleware:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.cors_origins_list,  # <-- Use the property here, not settings.CORS_ORIGINS
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )