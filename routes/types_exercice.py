# app/routes/types_exercice.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.type_exercice import TypeExercice
from schemas.type_exercice import TypeExerciceCreate, TypeExercice as TypeExerciceSchema
from core.security import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[TypeExerciceSchema])
def get_types_exercice(
    db: Session = Depends(get_db)
):
    types_exercice = db.query(TypeExercice).all()
    return types_exercice

@router.post("/", response_model=TypeExerciceSchema, status_code=status.HTTP_201_CREATED)
def create_type_exercice(
    type_exercice: TypeExerciceCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    # Dans un système complet, vous auriez une vérification des droits ici
    db_type_exercice = TypeExercice(**type_exercice.dict())
    db.add(db_type_exercice)
    db.commit()
    db.refresh(db_type_exercice)
    return db_type_exercice

@router.get("/{type_exercice_id}", response_model=TypeExerciceSchema)
def get_type_exercice(
    type_exercice_id: int, 
    db: Session = Depends(get_db)
):
    type_exercice = db.query(TypeExercice).filter(TypeExercice.id == type_exercice_id).first()
    if type_exercice is None:
        raise HTTPException(status_code=404, detail="Type d'exercice non trouvé")
    return type_exercice