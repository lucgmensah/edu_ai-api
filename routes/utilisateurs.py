# app/routes/utilisateurs.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.utilisateur import Utilisateur
from schemas.utilisateur import Utilisateur as UtilisateurSchema, UtilisateurCreate
from core.security import get_current_active_user, get_password_hash

router = APIRouter()

@router.get("/me", response_model=UtilisateurSchema)
def get_current_user_info(
    current_user: Utilisateur = Depends(get_current_active_user)
):
    return current_user

@router.get("/", response_model=List[UtilisateurSchema])
def get_utilisateurs(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    # Vérification simple: seuls les administrateurs pourraient avoir accès à cette liste
    # Dans une implémentation complète, vous auriez un système de rôles
    utilisateurs = db.query(Utilisateur).offset(skip).limit(limit).all()
    return utilisateurs

@router.get("/{utilisateur_id}", response_model=UtilisateurSchema)
def get_utilisateur(
    utilisateur_id: int, 
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    # On vérifie que l'utilisateur demande ses propres informations ou qu'il est admin
    if current_user.id != utilisateur_id:
        # Vérification d'admin: à implémenter selon votre logique d'autorisation
        pass
        
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

@router.put("/{utilisateur_id}", response_model=UtilisateurSchema)
def update_utilisateur(
    utilisateur_id: int,
    utilisateur_data: UtilisateurCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    # Vérification: un utilisateur ne peut modifier que son propre profil
    if current_user.id != utilisateur_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas autorisé à modifier ce profil"
        )

    db_utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if db_utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Mise à jour des champs
    db_utilisateur.nom = utilisateur_data.nom
    db_utilisateur.prenom = utilisateur_data.prenom
    db_utilisateur.email = utilisateur_data.email
    
    # Si un nouveau mot de passe est fourni
    if hasattr(utilisateur_data, "password") and utilisateur_data.password:
        db_utilisateur.hashed_password = get_password_hash(utilisateur_data.password)
    
    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur

@router.delete("/{utilisateur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_utilisateur(
    utilisateur_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    # Vérification: un utilisateur ne peut supprimer que son propre compte
    if current_user.id != utilisateur_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas autorisé à supprimer ce compte"
        )
        
    db_utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if db_utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    db.delete(db_utilisateur)
    db.commit()
    
    return {"detail": "Compte supprimé avec succès"}