from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.backend.database import Base

class AgentJob(Base):
    __tablename__ = "agent_jobs"

    id = Column(Integer, primary_key=True, index=True)
    input_image_data_url = Column(Text, nullable=True)
    input_text = Column(Text, nullable=False)
    status = Column(String, default="pending", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Output fields from the agent pipeline
    explanation = Column(Text, nullable=True)
    concepts = Column(Text, nullable=True)  # Could be JSON String
    storyboard = Column(Text, nullable=True)
    enhanced_storyboard = Column(Text, nullable=True)
    generated_code = Column(Text, nullable=True)
    review_comments = Column(Text, nullable=True)
    refactored_code = Column(Text, nullable=True)
    # manim_video_path = Column(String, nullable=True) # For later

    error_message = Column(Text, nullable=True) 