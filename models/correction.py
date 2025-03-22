# app/models/correction.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Correction(Base):
    __tablename__ = "corrections"
    
    id = Column(Integer, primary_key=True, index=True)
    solution = Column(String)
    explication = Column(String)
    question_id = Column(Integer, ForeignKey("questions.id"), unique=True)
    
    question = relationship("Question", back_populates="correction")
