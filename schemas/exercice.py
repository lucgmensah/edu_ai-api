# app/schemas/exercice.py
from pydantic import BaseModel
from typing import List, Optional
from .thematique import Thematique
from .type_exercice import TypeExercice

class ExerciceBase(BaseModel):
    titre: str
    description: Optional[str] = None
    difficulte: int
    duree_estimee: int
    thematique_id: int
    type_exercice_id: int

class ExerciceCreate(ExerciceBase):
    pass

class Exercice(ExerciceBase):
    id: int
    thematique: Optional[Thematique] = None
    type_exercice: Optional[TypeExercice] = None

    class Config:
        orm_mode = True