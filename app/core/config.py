import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Backend API"
    PORT: int = int(os.getenv("PORT", 8000))
    
    FIREBASE_CREDENTIALS_PATH: str = "firekeys.json"

    # Permite ignorar variables extras en el .env (como API_KEY, etc.)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
