from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models import Alerte, Capteur
from app.schema import AlerteCreate, AlerteResponse, AlerteUpdate
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/api/alertes", tags=["Alertes"])

@router.post("/", response_model=AlerteResponse)
def create_alerte(alerte: AlerteCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle alerte manuellement"""
    capteur = db.query(Capteur).filter(Capteur.id == alerte.capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    
    if alerte.niveau not in ["warning", "critical"]:
        raise HTTPException(status_code=400, detail="Niveau doit être 'warning' ou 'critical'")
    
    db_alerte = Alerte(**alerte.dict())
    db.add(db_alerte)
    db.commit()
    db.refresh(db_alerte)
    return db_alerte

@router.get("/", response_model=list[AlerteResponse])
def list_alertes(
    resolue: bool = Query(None, description="Filtrer par état résolu"),
    niveau: str = Query(None, description="Filtrer par niveau (warning/critical)"),
    limit: int = Query(100, description="Nombre max d'alertes à retourner"),
    db: Session = Depends(get_db)
):
    """Lister toutes les alertes avec filtres"""
    query = db.query(Alerte)
    
    if resolue is not None:
        query = query.filter(Alerte.resolue == resolue)
    
    if niveau:
        if niveau not in ["warning", "critical"]:
            raise HTTPException(status_code=400, detail="Niveau doit être 'warning' ou 'critical'")
        query = query.filter(Alerte.niveau == niveau)
    
    return query.order_by(Alerte.horodatage.desc()).limit(limit).all()

@router.get("/active", response_model=list[AlerteResponse])
def get_alertes_actives(db: Session = Depends(get_db)):
    """Récupérer uniquement les alertes non résolues"""
    return db.query(Alerte).filter(Alerte.resolue == False).order_by(Alerte.horodatage.desc()).all()

@router.get("/capteur/{capteur_id}", response_model=list[AlerteResponse])
def get_alertes_capteur(capteur_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Récupérer les alertes d'un capteur spécifique"""
    capteur = db.query(Capteur).filter(Capteur.id == capteur_id).first()
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    
    return db.query(Alerte).filter(
        Alerte.capteur_id == capteur_id
    ).order_by(Alerte.horodatage.desc()).limit(limit).all()

@router.get("/{alerte_id}", response_model=AlerteResponse)
def get_alerte(alerte_id: int, db: Session = Depends(get_db)):
    """Récupérer une alerte spécifique"""
    alerte = db.query(Alerte).filter(Alerte.id == alerte_id).first()
    if not alerte:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    return alerte

@router.put("/{alerte_id}/acquitter", response_model=AlerteResponse)
def acquitter_alerte(alerte_id: int, user_id: int, db: Session = Depends(get_db)):
    """Acquitter une alerte"""
    alerte = db.query(Alerte).filter(Alerte.id == alerte_id).first()
    if not alerte:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    alerte.acquitte_par = user_id
    alerte.acquitte_le = datetime.utcnow()
    db.commit()
    db.refresh(alerte)
    return alerte

@router.put("/{alerte_id}/resoudre", response_model=AlerteResponse)
def resoudre_alerte(alerte_id: int, db: Session = Depends(get_db)):
    """Marquer une alerte comme résolue"""
    alerte = db.query(Alerte).filter(Alerte.id == alerte_id).first()
    if not alerte:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    alerte.resolue = True
    db.commit()
    db.refresh(alerte)
    return alerte

@router.put("/{alerte_id}", response_model=AlerteResponse)
def update_alerte(alerte_id: int, update: AlerteUpdate, db: Session = Depends(get_db)):
    """Mettre à jour une alerte (acquitter/résoudre)"""
    alerte = db.query(Alerte).filter(Alerte.id == alerte_id).first()
    if not alerte:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    if update.acquitte_par is not None:
        alerte.acquitte_par = update.acquitte_par
        alerte.acquitte_le = datetime.utcnow()
    
    alerte.resolue = update.resolue
    db.commit()
    db.refresh(alerte)
    return alerte

@router.delete("/{alerte_id}")
def delete_alerte(alerte_id: int, db: Session = Depends(get_db)):
    """Supprimer une alerte"""
    alerte = db.query(Alerte).filter(Alerte.id == alerte_id).first()
    if not alerte:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    db.delete(alerte)
    db.commit()
    return {"message": "Alerte supprimée avec succès"}
