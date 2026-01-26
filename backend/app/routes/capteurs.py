from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Capteur
from app.schema import CapteurCreate, CapteurResponse
from app.database import get_db

router = APIRouter(prefix="/api/capteurs", tags=["Capteurs"])

@router.post("/", response_model=CapteurResponse)
def create_capteur(capteur: CapteurCreate, db: Session = Depends(get_db)):
    """Créer un nouveau capteur"""
    db_capteur = Capteur(**capteur.dict())
    db.add(db_capteur)
    db.commit()
    db.refresh(db_capteur)
    return db_capteur

@router.get("/", response_model=list[CapteurResponse])
def list_capteurs(db: Session = Depends(get_db)):
    """Lister tous les capteurs"""
    return db.query(Capteur).all()

@router.get("/{capteur_id}", response_model=CapteurResponse)
def get_capteur(capteur_id: int, db: Session = Depends(get_db)):
    """Récupérer un capteur spécifique"""
    capteur = db.query(Capteur).filter(Capteur.id == capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    return capteur
