# app/schemas/correction.py
from pydantic import BaseModel

class CorrectionBase(BaseModel):
    solution: str
    explication: str
    question_id: int

class CorrectionCreate(CorrectionBase):
    pass

class Correction(CorrectionBase):
    id: int

    class Config:
        orm_mode = True