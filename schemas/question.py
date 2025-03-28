# app/schemas/question.py
from pydantic import BaseModel
from typing import Optional

class OptionSchema(BaseModel):
    id: int
    option: str
    question_id: int

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    enonce: str
    points_max: int
    exercice_id: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    options: Optional[list[OptionSchema]] = []

    class Config:
        orm_mode = True