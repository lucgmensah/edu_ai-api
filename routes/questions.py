# app/routes/questions.py contient aussi  les routes pour les corrections des questions
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.question import Question
from models.correction import Correction
from schemas.question import QuestionCreate, Question as QuestionSchema
from schemas.correction import CorrectionCreate, Correction as CorrectionSchema
from core.security import get_current_active_user

router = APIRouter()

@router.get("/exercice/{exercice_id}", response_model=List[QuestionSchema])
def get_questions_by_exercice(
    exercice_id: int,
    db: Session = Depends(get_db)
):
    questions = db.query(Question).filter(Question.exercice_id == exercice_id).all()
    return questions

@router.post("/", response_model=QuestionSchema, status_code=status.HTTP_201_CREATED)
def create_question(
    question: QuestionCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    # Dans un système complet, vous auriez une vérification des droits ici
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/{question_id}", response_model=QuestionSchema)
def get_question(
    question_id: int, 
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    return question

@router.put("/{question_id}", response_model=QuestionSchema)
def update_question(
    question_id: int,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    
    # Mise à jour des champs
    for key, value in question_data.dict().items():
        setattr(db_question, key, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    
    db.delete(db_question)
    db.commit()
    return {"detail": "Question supprimée avec succès"}

# Routes pour les corrections
@router.post("/{question_id}/correction", response_model=CorrectionSchema, status_code=status.HTTP_201_CREATED)
def create_correction(
    question_id: int,
    correction: CorrectionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    # Vérifier que la question existe
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    
    # Vérifier si une correction existe déjà
    existing_correction = db.query(Correction).filter(Correction.question_id == question_id).first()
    if existing_correction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Une correction existe déjà pour cette question"
        )
    
    # Créer la nouvelle correction
    db_correction = Correction(**correction.dict())
    db.add(db_correction)
    db.commit()
    db.refresh(db_correction)
    return db_correction

@router.get("/{question_id}/correction", response_model=CorrectionSchema)
def get_correction(
    question_id: int,
    db: Session = Depends(get_db)
):
    correction = db.query(Correction).filter(Correction.question_id == question_id).first()
    if correction is None:
        raise HTTPException(status_code=404, detail="Correction non trouvée")
    return correction

@router.put("/{question_id}/correction", response_model=CorrectionSchema)
def update_correction(
    question_id: int,
    correction_data: CorrectionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    correction = db.query(Correction).filter(Correction.question_id == question_id).first()
    if correction is None:
        raise HTTPException(status_code=404, detail="Correction non trouvée")
    
    # Mise à jour des champs
    correction.solution = correction_data.solution
    correction.explication = correction_data.explication
    
    db.commit()
    db.refresh(correction)
    return correction