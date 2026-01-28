from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Capteur
from app.schema import CapteurCreate, CapteurResponse, CapteurUpdate
from app.database import get_db

router = APIRouter(prefix="/api/capteurs", tags=["Capteurs"])

@router.post("/", response_model=CapteurResponse, status_code=201)
def create_capteur(capteur: CapteurCreate, db: Session = Depends(get_db)):
    """Créer un nouveau capteur avec ID spécifié par Arduino"""
    
    # Vérifier si l'ID existe déjà
    existing = db.query(Capteur).filter(Capteur.id == capteur.id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Capteur avec ID {capteur.id} existe déjà")
    
    db_capteur = Capteur(**capteur.dict())
    db.add(db_capteur)
    db.commit()
    db.refresh(db_capteur)
    return db_capteur

@router.get("/", response_model=list[CapteurResponse])
def list_capteurs(actif: bool = None, db: Session = Depends(get_db)):
    """Lister tous les capteurs"""
    query = db.query(Capteur)
    if actif is not None:
        query = query.filter(Capteur.actif == actif)
    return query.all()

@router.get("/{capteur_id}", response_model=CapteurResponse)
def get_capteur(capteur_id: int, db: Session = Depends(get_db)):
    """Récupérer un capteur spécifique"""
    capteur = db.query(Capteur).filter(Capteur.id == capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    return capteur

@router.put("/{capteur_id}", response_model=CapteurResponse)
def update_capteur(capteur_id: int, update: CapteurUpdate, db: Session = Depends(get_db)):
    """Mettre à jour un capteur"""
    capteur = db.query(Capteur).filter(Capteur.id == capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(capteur, key, value)
    
    db.commit()
    db.refresh(capteur)
    return capteur

@router.delete("/{capteur_id}")
def delete_capteur(capteur_id: int, db: Session = Depends(get_db)):
    """Supprimer un capteur"""
    capteur = db.query(Capteur).filter(Capteur.id == capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    
    db.delete(capteur)
    db.commit()
    return {"message": "Capteur supprimé avec succès"}
