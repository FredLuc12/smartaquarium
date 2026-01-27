from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Mesure, Capteur, Alerte
from app.schema import MesureCreate, MesureResponse
from app.database import get_db

router = APIRouter(prefix="/api/mesures", tags=["Mesures"])

@router.post("/", response_model=MesureResponse)
def create_mesure(mesure: MesureCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle mesure et vérifier les seuils"""
    # Vérifier que le capteur existe
    capteur = db.query(Capteur).filter(Capteur.id == mesure.capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    
    # Créer la mesure
    db_mesure = Mesure(**mesure.dict())
    db.add(db_mesure)
    db.commit()
    db.refresh(db_mesure)
    
    # Vérifier les seuils et créer une alerte si nécessaire
    if capteur.actif and (capteur.seuil_min is not None or capteur.seuil_max is not None):
        alerte_message = None
        niveau = None
        
        if capteur.seuil_min is not None and mesure.valeur < capteur.seuil_min:
            niveau = "warning"
            alerte_message = f"{capteur.nom}: valeur trop basse ({mesure.valeur} {capteur.unite} < {capteur.seuil_min})"
        elif capteur.seuil_max is not None and mesure.valeur > capteur.seuil_max:
            niveau = "critical"
            alerte_message = f"{capteur.nom}: valeur trop haute ({mesure.valeur} {capteur.unite} > {capteur.seuil_max})"
        
        if alerte_message:
            alerte = Alerte(
                capteur_id=capteur.id,
                niveau=niveau,
                message=alerte_message
            )
            db.add(alerte)
            db.commit()
    
    return db_mesure

@router.get("/", response_model=list[MesureResponse])
def list_mesures(limit: int = 100, db: Session = Depends(get_db)):
    """Lister toutes les mesures récentes"""
    return db.query(Mesure).order_by(Mesure.horodatage.desc()).limit(limit).all()

@router.get("/capteur/{capteur_id}", response_model=list[MesureResponse])
def get_mesures_capteur(capteur_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Récupérer les mesures d'un capteur spécifique"""
    capteur = db.query(Capteur).filter(Capteur.id == capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    
    return db.query(Mesure).filter(
        Mesure.capteur_id == capteur_id
    ).order_by(Mesure.horodatage.desc()).limit(limit).all()

@router.get("/capteur/{capteur_id}/latest", response_model=MesureResponse)
def get_latest_mesure(capteur_id: int, db: Session = Depends(get_db)):
    """Récupérer la dernière mesure d'un capteur"""
    capteur = db.query(Capteur).filter(Capteur.id == capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    
    mesure = db.query(Mesure).filter(
        Mesure.capteur_id == capteur_id
    ).order_by(Mesure.horodatage.desc()).first()
    
    if not mesure:
        raise HTTPException(status_code=404, detail="Aucune mesure trouvée")
    
    return mesure
