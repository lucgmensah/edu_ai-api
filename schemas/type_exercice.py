# app/schemas/type_exercice.py
from pydantic import BaseModel
from typing import Optional

class TypeExerciceBase(BaseModel):
    nom: str
    description: Optional[str] = None

class TypeExerciceCreate(TypeExerciceBase):
    pass

class TypeExercice(TypeExerciceBase):
    id: int

    class Config:
        orm_mode = True