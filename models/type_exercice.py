# app/models/type_exercice.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class TypeExercice(Base):
    __tablename__ = "types_exercice"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    description = Column(String)
    
    exercices = relationship("Exercice", back_populates="type_exercice")