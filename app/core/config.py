# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    GEN_API_KEY: str
    GEN_MODEL_ID: str = "gpt-4-1"

    class Config:
        env_file = ".env"

settings = Settings()