from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import HistoriqueCommande, Actionneur
from app.schema import CommandeCreate, CommandeResponse
from app.database import get_db

router = APIRouter(prefix="/api/commandes", tags=["Commandes"])

@router.post("/", response_model=CommandeResponse)
def create_commande(commande: CommandeCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle commande et mettre à jour l'actionneur"""
    actionneur = db.query(Actionneur).filter(Actionneur.id == commande.actionneur_id).first()
    if not actionneur:
        raise HTTPException(status_code=404, detail="Actionneur non trouvé")
    
    if commande.commande not in ["ON", "OFF"]:
        raise HTTPException(status_code=400, detail="Commande doit être 'ON' ou 'OFF'")
    
    # Mettre à jour l'état de l'actionneur
    actionneur.etat = (commande.commande == "ON")
    
    # Enregistrer la commande dans l'historique
    db_commande = HistoriqueCommande(**commande.dict())
    db.add(db_commande)
    db.commit()
    db.refresh(db_commande)
    return db_commande

@router.get("/", response_model=list[CommandeResponse])
def list_commandes(limit: int = 100, db: Session = Depends(get_db)):
    """Lister toutes les commandes"""
    return db.query(HistoriqueCommande).order_by(HistoriqueCommande.horodatage.desc()).limit(limit).all()

@router.get("/actionneur/{actionneur_id}", response_model=list[CommandeResponse])
def get_commandes_actionneur(actionneur_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Lister les commandes d'un actionneur spécifique"""
    actionneur = db.query(Actionneur).filter(Actionneur.id == actionneur_id).first()
    if not actionneur:
        raise HTTPException(status_code=404, detail="Actionneur non trouvé")
    
    return db.query(HistoriqueCommande).filter(
        HistoriqueCommande.actionneur_id == actionneur_id
    ).order_by(HistoriqueCommande.horodatage.desc()).limit(limit).all()
