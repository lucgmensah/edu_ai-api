# app/models/question.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    enonce = Column(String)
    points_max = Column(Integer)
    exercice_id = Column(Integer, ForeignKey("exercices.id"))
    
    options = relationship("Option", back_populates="question")
    exercice = relationship("Exercice", back_populates="questions")
    correction = relationship("Correction", back_populates="question", uselist=False)
    reponses_utilisateur = relationship("ReponseUtilisateur", back_populates="question")