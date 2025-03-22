# app/schemas/reponse_utilisateur.py
from pydantic import BaseModel
from typing import Optional

class ReponseUtilisateurBase(BaseModel):
    contenu: str
    tentative_id: int
    question_id: int

class ReponseUtilisateurCreate(ReponseUtilisateurBase):
    pass

class ReponseUtilisateur(ReponseUtilisateurBase):
    id: int
    est_correcte: Optional[bool] = None
    points: Optional[int] = None

    class Config:
        orm_mode = True