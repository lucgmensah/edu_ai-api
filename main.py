# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import utilisateur, thematique, type_exercice, exercice, question, correction, tentative, reponse_utilisateur
from routes import auth, utilisateurs, exercices, questions, tentatives, thematiques, types_exercice

# Création des tables dans la base de données
models = [utilisateur, thematique, type_exercice, exercice, question, correction, tentative, reponse_utilisateur]
for model in models:
    model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ExercicesAPI",
    description="API pour une application d'exercices éducatifs",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # A remplacer par l'URL de votre frontend en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(auth.router, tags=["authentication"])
app.include_router(utilisateurs.router, prefix="/utilisateurs", tags=["utilisateurs"])
app.include_router(thematiques.router, prefix="/thematiques", tags=["thematiques"])
app.include_router(exercices.router, prefix="/exercices", tags=["exercices"])
app.include_router(questions.router, prefix="/questions", tags=["questions"])
app.include_router(tentatives.router, prefix="/tentatives", tags=["tentatives"])
app.include_router(types_exercice.router, prefix="/types_exercice", tags=["types_exercice"])

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API d'exercices éducatifs"}