from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Index, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Capteur(Base):
    __tablename__ = "capteurs"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    unite = Column(String(20), nullable=False)
    localisation = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<Capteur {self.id}: {self.nom}>"

class Actionneur(Base):
    __tablename__ = "actionneurs"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    etat = Column(Boolean, default=False)
    derniere_mise_a_jour = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Actionneur {self.id}: {self.nom}>"

class Mesure(Base):
    __tablename__ = "mesures"
    __table_args__ = (
        Index('idx_mesures_capteur_id', 'capteur_id'),
        Index('idx_mesures_horodatage', 'horodatage'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    capteur_id = Column(Integer, ForeignKey("capteurs.id", ondelete="CASCADE"), nullable=False)
    valeur = Column(Float, nullable=False)
    horodatage = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Mesure {self.id}: {self.valeur} @ {self.horodatage}>"

class HistoriqueCommande(Base):
    __tablename__ = "historique_commandes"
    __table_args__ = (
        Index('idx_hist_cmd_actionneur_id', 'actionneur_id'),
        Index('idx_hist_cmd_horodatage', 'horodatage'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    actionneur_id = Column(Integer, ForeignKey("actionneurs.id", ondelete="CASCADE"), nullable=False)
    commande = Column(String(10), nullable=False)  # 'ON', 'OFF'
    source = Column(String(50), nullable=False)     # 'front', 'auto', 'arduino'
    horodatage = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Commande {self.id}: {self.commande} @ {self.horodatage}>"
