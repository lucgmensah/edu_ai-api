# app/models/thematique.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Thematique(Base):
    __tablename__ = "thematiques"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    description = Column(String)
    
    exercices = relationship("Exercice", back_populates="thematique")
