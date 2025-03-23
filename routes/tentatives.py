# app/routes/tentatives.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models.tentative import Tentative
from models.reponse_utilisateur import ReponseUtilisateur
from models.question import Question
from models.correction import Correction
from schemas.tentative import TentativeCreate, Tentative as TentativeSchema
from schemas.reponse_utilisateur import ReponseUtilisateurCreate
from core.security import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[TentativeSchema])
def get_user_tentatives(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    tentatives = db.query(Tentative).filter(Tentative.utilisateur_id == current_user.id).all()
    return tentatives

@router.post("/", response_model=TentativeSchema, status_code=status.HTTP_201_CREATED)
def create_tentative(
    tentative: TentativeCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_tentative = Tentative(**tentative.dict(), utilisateur_id=current_user.id)
    db.add(db_tentative)
    db.commit()
    db.refresh(db_tentative)
    return db_tentative

@router.post("/{tentative_id}/reponses")
def submit_response(
    tentative_id: int,
    reponse: ReponseUtilisateurCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    # Vérifier que la tentative existe et appartient à l'utilisateur
    tentative = db.query(Tentative).filter(
        Tentative.id == tentative_id,
        Tentative.utilisateur_id == current_user.id
    ).first()
    
    if not tentative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tentative non trouvée ou non autorisée"
        )
    
    # Vérifier que la question appartient à l'exercice de la tentative
    question = db.query(Question).filter(
        Question.id == reponse.question_id,
        Question.exercice_id == tentative.exercice_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question invalide pour cet exercice"
        )
    
    # Créer la réponse
    db_reponse = ReponseUtilisateur(
        contenu=reponse.contenu,
        tentative_id=tentative_id,
        question_id=reponse.question_id
    )
    
    # Vérifier la réponse et attribuer des points
    correction = db.query(Correction).filter(Correction.question_id == reponse.question_id).first()
    if correction:
        # Logique simplifiée pour la vérification des réponses
        # Dans un cas réel, cette logique serait plus complexe selon le type d'exercice
        if reponse.contenu.lower() == correction.solution.lower():
            db_reponse.est_correcte = True
            db_reponse.points = question.points_max
        else:
            db_reponse.est_correcte = False
            db_reponse.points = 0
    
    db.add(db_reponse)
    db.commit()
    db.refresh(db_reponse)
    
    return {
        "id": db_reponse.id,
        "est_correcte": db_reponse.est_correcte,
        "points": db_reponse.points
    }

@router.post("/{tentative_id}/terminer")
def complete_tentative(
    tentative_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    # Vérifier que la tentative existe et appartient à l'utilisateur
    tentative = db.query(Tentative).filter(
        Tentative.id == tentative_id,
        Tentative.utilisateur_id == current_user.id
    ).first()
    
    if not tentative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tentative non trouvée ou non autorisée"
        )
    
    # Marquer la tentative comme terminée
    tentative.date_fin = datetime.utcnow()
    
    # Calculer la note finale
    reponses = db.query(ReponseUtilisateur).filter(ReponseUtilisateur.tentative_id == tentative_id).all()
    
    total_points = 0
    max_points = 0
    
    for reponse in reponses:
        question = db.query(Question).filter(Question.id == reponse.question_id).first()
        if question:
            max_points += question.points_max
            total_points += reponse.points if reponse.points is not None else 0
    
    if max_points > 0:
        tentative.note_finale = (total_points / max_points) * 20  # Note sur 20
    else:
        tentative.note_finale = 0
    
    db.commit()
    db.refresh(tentative)
    
    return {
        "tentative_id": tentative.id,
        "date_debut": tentative.date_debut,
        "date_fin": tentative.date_fin,
        "note_finale": tentative.note_finale,
        "points_obtenus": total_points,
        "points_max": max_points
    }