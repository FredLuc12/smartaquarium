from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ===== CAPTEURS =====
class CapteurBase(BaseModel):
    nom: str
    type: str
    unite: str
    localisation: Optional[str] = None

class CapteurCreate(CapteurBase):
    pass

class CapteurResponse(CapteurBase):
    id: int
    
    class Config:
        from_attributes = True

# ===== MESURES =====
class MesureBase(BaseModel):
    capteur_id: int
    valeur: float

class MesureCreate(MesureBase):
    pass

class MesureResponse(MesureBase):
    id: int
    horodatage: datetime
    
    class Config:
        from_attributes = True

# ===== ACTIONNEURS =====
class ActionneurBase(BaseModel):
    nom: str
    type: str
    etat: bool = False

class ActionneurCreate(ActionneurBase):
    pass

class ActionneurUpdate(BaseModel):
    etat: bool

class ActionneurResponse(ActionneurBase):
    id: int
    derniere_mise_a_jour: datetime
    
    class Config:
        from_attributes = True

# ===== COMMANDES =====
class CommandeCreate(BaseModel):
    actionneur_id: int
    commande: str  # 'ON', 'OFF'
    source: str = "api"

class CommandeResponse(CommandeCreate):
    id: int
    horodatage: datetime
    
    class Config:
        from_attributes = True
