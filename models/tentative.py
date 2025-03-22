# app/models/tentative.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Tentative(Base):
    __tablename__ = "tentatives"
    
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    exercice_id = Column(Integer, ForeignKey("exercices.id"))
    date_debut = Column(DateTime, default=datetime.utcnow)
    date_fin = Column(DateTime, nullable=True)
    note_finale = Column(Float, nullable=True)
    
    utilisateur = relationship("Utilisateur", back_populates="tentatives")
    exercice = relationship("Exercice", back_populates="tentatives")
    reponses = relationship("ReponseUtilisateur", back_populates="tentative")
