from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import capteurs, mesures, actionneurs

# Créer l'app
app = FastAPI(title="SmartAquarium API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(capteurs.router)
app.include_router(mesures.router)
app.include_router(actionneurs.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.environment}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
