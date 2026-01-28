from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# ===== CAPTEURS =====
class CapteurBase(BaseModel):
    id: int = Field(..., description="ID du capteur (défini par Arduino)")
    nom: str
    type: str
    unite: str
    localisation: Optional[str] = None
    seuil_min: Optional[float] = None
    seuil_max: Optional[float] = None
    actif: bool = True

class CapteurCreate(CapteurBase):
    pass

class CapteurUpdate(BaseModel):
    nom: Optional[str] = None
    type: Optional[str] = None
    unite: Optional[str] = None
    localisation: Optional[str] = None
    seuil_min: Optional[float] = None
    seuil_max: Optional[float] = None
    actif: Optional[bool] = None

class CapteurResponse(CapteurBase):
    class Config:
        from_attributes = True

# ===== ACTIONNEURS =====
class ActionneurBase(BaseModel):
    id: int = Field(..., description="ID de l'actionneur (défini par Arduino)")
    nom: str
    type: str
    etat: bool = False

class ActionneurCreate(ActionneurBase):
    pass

class ActionneurUpdate(BaseModel):
    etat: bool

class ActionneurResponse(ActionneurBase):
    derniere_mise_a_jour: datetime
    
    class Config:
        from_attributes = True

# ===== MESURES (pas de changement) =====
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

# ===== COMMANDES (pas de changement) =====
class CommandeCreate(BaseModel):
    actionneur_id: int
    commande: str = Field(..., pattern="^(ON|OFF)$")
    source: str = "api"

class CommandeResponse(CommandeCreate):
    id: int
    horodatage: datetime
    
    class Config:
        from_attributes = True

# ===== ALERTES (pas de changement) =====
class AlerteBase(BaseModel):
    capteur_id: int
    niveau: str = Field(..., pattern="^(warning|critical)$")
    message: str

class AlerteCreate(AlerteBase):
    pass

class AlerteUpdate(BaseModel):
    acquitte_par: Optional[int] = None
    resolue: bool = False

class AlerteResponse(AlerteBase):
    id: int
    horodatage: datetime
    acquitte_par: Optional[int] = None
    acquitte_le: Optional[datetime] = None
    resolue: bool
    
    class Config:
        from_attributes = True
