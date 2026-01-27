from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Capteur, Actionneur, Mesure, HistoriqueCommande, Alerte
from app.routes import capteurs, mesures, actionneurs, commandes, alertes
from app.config import settings

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartAquarium API",
    description="API de gestion d'aquarium connecté avec capteurs et actionneurs",
    version="1.0.0"
)

# CORS - Important pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, remplacer par l'URL du frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure toutes les routes
app.include_router(capteurs.router)
app.include_router(mesures.router)
app.include_router(actionneurs.router)
app.include_router(commandes.router)
app.include_router(alertes.router)

@app.get("/")
def root():
    """Point d'entrée de l'API"""
    return {
        "message": "SmartAquarium API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    """Vérifier l'état de l'API"""
    return {
        "status": "ok",
        "environment": settings.environment,
        "debug": settings.debug
    }
