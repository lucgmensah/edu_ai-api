# app/schemas/utilisateur.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UtilisateurBase(BaseModel):
    email: EmailStr
    nom: str
    prenom: str

class UtilisateurCreate(UtilisateurBase):
    password: str

class Utilisateur(UtilisateurBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True