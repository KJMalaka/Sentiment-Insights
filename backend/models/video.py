from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VideoAnalysis(Base):
    __tablename__ = "video_analysis"

    video_id = Column(String, primary_key=True, index=True)
    platform = Column(String) # e.g., "youtube"
    analysis_json = Column(Text) # Store the complete result JSON
