# app/schemas/question.py
from pydantic import BaseModel
from typing import Optional

class QuestionBase(BaseModel):
    enonce: str
    points_max: int
    exercice_id: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True