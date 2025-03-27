# app/routes/exercices.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.correction import Correction
from models.exercice import Exercice
from models.question import Question
from rag import rag
from schemas.exercice import ExerciceCreate, Exercice as ExerciceSchema
from models.tentative import Tentative
from core.security import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[ExerciceSchema])
def get_exercices(
    skip: int = 0, 
    limit: int = 100, 
    thematique_id: int = None,
    type_exercice_id: int = None,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_active_user)
):
    query = db.query(Exercice).join(Tentative).filter(Tentative.utilisateur_id == user.id)
    
    if thematique_id:
        query = query.filter(Exercice.thematique_id == thematique_id)
    
    if type_exercice_id:
        query = query.filter(Exercice.type_exercice_id == type_exercice_id)
    
    exercices = query.offset(skip).limit(limit).all()
    return exercices

@router.post("/", response_model=ExerciceSchema, status_code=status.HTTP_201_CREATED)
def create_exercice(
    exercice: ExerciceCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_exercice = Exercice(**exercice.dict(), createur_id=current_user.id)
    db.add(db_exercice)
    db.commit()
    db.refresh(db_exercice)
    
    questions = rag.generate_questions(db_exercice.type_exercice_id.nom, db_exercice.difficulte)
    
    for question in questions:
        db_question = Question(enonce=question["question"]+" "+question["choices"], points_max=10/len(questions), exercice_id=db_exercice.id)
        if db_exercice.type_exercice_id.nom == "QCM":
            db_corrections = Correction(solution=question["correct"], question_id=db_question.id)
        
        db.add(db_question)
    
    return db_exercice

@router.get("/{exercice_id}", response_model=ExerciceSchema)
def get_exercice(
    exercice_id: int, 
    db: Session = Depends(get_db)
):
    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()
    if exercice is None:
        raise HTTPException(status_code=404, detail="Exercice non trouvé")
    return exercice