# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Campos que a nossa aplicação REALMENTE precisa ler do .env
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    
    # --- A CORREÇÃO ESTÁ AQUI ---
    # Adicionamos os campos que o Celery precisa ler do .env
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    # ---------------------------

    FIREBASE_CREDENTIALS_PATH: str | None = None

    # A model_config do Pydantic V2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()