from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./aquarium.db")
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    port: int = int(os.getenv("PORT", 8000))

    class Config:
        env_file = ".env"

settings = Settings()
