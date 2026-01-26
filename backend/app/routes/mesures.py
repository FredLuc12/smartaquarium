from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Mesure, Capteur
from app.schema import MesureCreate, MesureResponse
from app.database import get_db

router = APIRouter(prefix="/api/mesures", tags=["Mesures"])

@router.post("/", response_model=MesureResponse)
def create_mesure(mesure: MesureCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle mesure (reçue de l'Arduino)"""
    # Vérifier que le capteur existe
    capteur = db.query(Capteur).filter(Capteur.id == mesure.capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    
    db_mesure = Mesure(**mesure.dict())
    db.add(db_mesure)
    db.commit()
    db.refresh(db_mesure)
    return db_mesure

@router.get("/", response_model=list[MesureResponse])
def list_mesures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lister toutes les mesures (avec pagination)"""
    return db.query(Mesure).offset(skip).limit(limit).all()

@router.get("/capteur/{capteur_id}", response_model=list[MesureResponse])
def get_mesures_capteur(capteur_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Récupérer l'historique des mesures d'un capteur"""
    return db.query(Mesure).filter(Mesure.capteur_id == capteur_id).order_by(Mesure.horodatage.desc()).limit(limit).all()
