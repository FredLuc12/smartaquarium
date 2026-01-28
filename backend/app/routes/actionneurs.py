from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Actionneur, HistoriqueCommande
from app.schema import ActionneurCreate, ActionneurResponse, ActionneurUpdate, CommandeResponse
from app.database import get_db

router = APIRouter(prefix="/api/actionneurs", tags=["Actionneurs"])

@router.post("/", response_model=ActionneurResponse, status_code=201)
def create_actionneur(actionneur: ActionneurCreate, db: Session = Depends(get_db)):
    """Créer un nouvel actionneur avec ID spécifié par Arduino"""
    
    # Vérifier si l'ID existe déjà
    existing = db.query(Actionneur).filter(Actionneur.id == actionneur.id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Actionneur avec ID {actionneur.id} existe déjà")
    
    db_actionneur = Actionneur(**actionneur.dict())
    db.add(db_actionneur)
    db.commit()
    db.refresh(db_actionneur)
    return db_actionneur

@router.get("/", response_model=list[ActionneurResponse])
def list_actionneurs(db: Session = Depends(get_db)):
    """Lister tous les actionneurs"""
    return db.query(Actionneur).all()

@router.get("/{actionneur_id}", response_model=ActionneurResponse)
def get_actionneur(actionneur_id: int, db: Session = Depends(get_db)):
    """Récupérer un actionneur spécifique"""
    actionneur = db.query(Actionneur).filter(Actionneur.id == actionneur_id).first()
    if not actionneur:
        raise HTTPException(status_code=404, detail="Actionneur non trouvé")
    return actionneur

@router.put("/{actionneur_id}", response_model=ActionneurResponse)
def update_actionneur_state(actionneur_id: int, update: ActionneurUpdate, db: Session = Depends(get_db)):
    """Mettre à jour l'état d'un actionneur"""
    actionneur = db.query(Actionneur).filter(Actionneur.id == actionneur_id).first()
    if not actionneur:
        raise HTTPException(status_code=404, detail="Actionneur non trouvé")
    
    actionneur.etat = update.etat
    db.add(actionneur)
    db.commit()
    db.refresh(actionneur)
    
    # Enregistrer la commande
    commande = HistoriqueCommande(
        actionneur_id=actionneur_id,
        commande="ON" if update.etat else "OFF",
        source="api"
    )
    db.add(commande)
    db.commit()
    
    return actionneur

@router.get("/{actionneur_id}/historique", response_model=list[CommandeResponse])
def get_historique_actionneur(actionneur_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Récupérer l'historique des commandes d'un actionneur"""
    return db.query(HistoriqueCommande).filter(
        HistoriqueCommande.actionneur_id == actionneur_id
    ).order_by(HistoriqueCommande.horodatage.desc()).limit(limit).all()
