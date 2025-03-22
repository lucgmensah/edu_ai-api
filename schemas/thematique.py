# app/schemas/thematique.py
from pydantic import BaseModel
from typing import List, Optional

class ThematiqueBase(BaseModel):
    nom: str
    description: Optional[str] = None

class ThematiqueCreate(ThematiqueBase):
    pass

class Thematique(ThematiqueBase):
    id: int

    class Config:
        orm_mode = True