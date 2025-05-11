# app/backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
from pydantic import PostgresDsn, ValidationError

# First, try to import settings. If this fails, we'll use a fallback.
try:
    from app.backend.config import settings
    
    # Attempt to get DATABASE_URL and create engine
    try:
        # Convert to string in case it's a PostgresDsn object
        db_url = str(settings.DATABASE_URL)
        print(f"Using database URL: {db_url.split('@')[0].replace('postgresql://', '***:***@')}@{db_url.split('@')[1] if '@' in db_url else '***'}")
        engine = create_engine(db_url)
    except (AttributeError, ValidationError, Exception) as e:
        # If settings.DATABASE_URL is missing, invalid, or connection fails
        print(f"Error connecting to configured database: {str(e)}", file=sys.stderr)
        print("⚠️ Using SQLite in-memory database as fallback. This should only be used for development.", file=sys.stderr)
        engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
except ImportError as e:
    print(f"Error importing config: {str(e)}", file=sys.stderr)
    print("⚠️ Using SQLite in-memory database as fallback. This should only be used for development.", file=sys.stderr)
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})

# Create a SessionLocal class that will be used to create a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

# Dependency function to get a database session
def get_db():
    """
    Dependency for FastAPI endpoints that need a database session.
    
    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()