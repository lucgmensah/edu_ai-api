# app/models/reponse_utilisateur.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ReponseUtilisateur(Base):
    __tablename__ = "reponses_utilisateur"
    
    id = Column(Integer, primary_key=True, index=True)
    contenu = Column(String)
    est_correcte = Column(Boolean, nullable=True)
    points = Column(Integer, nullable=True)
    tentative_id = Column(Integer, ForeignKey("tentatives.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    tentative = relationship("Tentative", back_populates="reponses")
    question = relationship("Question", back_populates="reponses_utilisateur")