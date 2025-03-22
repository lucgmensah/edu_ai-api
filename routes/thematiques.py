# app/routes/thematiques.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.thematique import Thematique
from schemas.thematique import ThematiqueCreate, Thematique as ThematiqueSchema
from core.security import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[ThematiqueSchema])
def get_thematiques(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    thematiques = db.query(Thematique).offset(skip).limit(limit).all()
    return thematiques

@router.post("/", response_model=ThematiqueSchema, status_code=status.HTTP_201_CREATED)
def create_thematique(
    thematique: ThematiqueCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_thematique = Thematique(**thematique.dict())
    db.add(db_thematique)
    db.commit()
    db.refresh(db_thematique)
    return db_thematique

@router.get("/{thematique_id}", response_model=ThematiqueSchema)
def get_thematique(
    thematique_id: int, 
    db: Session = Depends(get_db)
):
    thematique = db.query(Thematique).filter(Thematique.id == thematique_id).first()
    if thematique is None:
        raise HTTPException(status_code=404, detail="Thématique non trouvée")
    return thematique