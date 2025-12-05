from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "profiles-service"
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    SUBSCRIPTIONS_BASE_URL: str  # URL pública de tu subscriptions-service

    class Config:
        env_file = ".env"

settings = Settings()
