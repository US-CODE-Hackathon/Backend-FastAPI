from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from db import Base


class EmotionalReport(Base):
    __tablename__ = "emotional_report"
    emotional_report_id = Column(Integer, primary_key=True, index=True)
    is_first = Column(Boolean)
    conversation_id = Column(Integer)
    created_at = Column(DateTime)
    image_url = Column(Text)
    sentiment = Column(String(50))
    summary = Column(Text)
    title = Column(String(255))
