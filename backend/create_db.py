# create_db.py
from app.main import app, engine, Base
from app.models import *

print("🔨 Création DB...")
Base.metadata.create_all(bind=engine)
print("✅ Tables créées ! Vérifie avec ls *.db")
