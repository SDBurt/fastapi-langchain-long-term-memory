# app/models/memory.py

from sqlalchemy import Column, Integer, String, Text, Boolean
from app.utils.database import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    response = Column(Text)
    long_term = Column(Boolean, default=False)