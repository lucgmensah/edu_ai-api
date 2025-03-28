# app/routes/exercices.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.correction import Correction
from models.exercice import Exercice
from models.option import Option
from models.question import Question
from models.type_exercice import TypeExercice  # Import the Type_Exercice model
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
    
    type = db.query(TypeExercice).filter(TypeExercice.id == db_exercice.type_exercice_id).first()
    
    questions = rag.generate_questions(type.nom, db_exercice.thematique.nom, db_exercice.difficulte, 5)
    
    print(questions)
    
    for question in questions:
        print(question["question"])
        db_question = Question(enonce=question["question"], points_max=10/len(questions), exercice_id=db_exercice.id)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        if type.nom == "QCM":
            for key, option in question["choices"].items():
                print(option)
                db_option = Option(option=option, question_id=db_question.id)
                db.add(db_option)
                db.commit()
                db.refresh(db_option)
                
            print(question["correct"])
            db_corrections = Correction(solution=question["correct"], question_id=db_question.id)
            db.add(db_corrections)
            db.commit()
            db.refresh(db_corrections)
    
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