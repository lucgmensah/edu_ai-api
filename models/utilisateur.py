# app/models/utilisateur.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    tentatives = relationship("Tentative", back_populates="utilisateur")