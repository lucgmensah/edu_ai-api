# app/schemas/tentative.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TentativeBase(BaseModel):
    utilisateur_id: int
    exercice_id: int

class TentativeCreate(TentativeBase):
    pass

class Tentative(TentativeBase):
    id: int
    date_debut: datetime
    date_fin: Optional[datetime] = None
    note_finale: Optional[float] = None

    class Config:
        orm_mode = True