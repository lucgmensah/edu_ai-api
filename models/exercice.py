# app/models/exercice.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Exercice(Base):
    __tablename__ = "exercices"
    
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    description = Column(String)
    difficulte = Column(Integer)
    duree_estimee = Column(Integer)  # en minutes
    thematique_id = Column(Integer, ForeignKey("thematiques.id"))
    type_exercice_id = Column(Integer, ForeignKey("types_exercice.id"))
    
    thematique = relationship("Thematique", back_populates="exercices")
    type_exercice = relationship("TypeExercice", back_populates="exercices")
    questions = relationship("Question", back_populates="exercice")
    tentatives = relationship("Tentative", back_populates="exercice")
