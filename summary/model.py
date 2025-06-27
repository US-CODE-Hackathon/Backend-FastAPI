from sqlalchemy import Column, Integer, String, Text, DateTime
from db import Base


class Summary(Base):
    __tablename__ = "summary"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    sentiment = Column(String(50))
    summary = Column(Text)
    photo = Column(Text)
    date = Column(DateTime)
