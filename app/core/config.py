from pydantic_settings import BaseSettings
import os


env_path = '.env'

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    APP_HOST: str
    APP_PORT: int
    LOG_LEVEL: str = "INFO"
    APP_NAME: str = "n8nback"
    APP_VERSION: str = "0.1.0"

    N8N_WEBHOOK_URL: str

    class Config:
        env_file = env_path
        extra = 'ignore'

settings = Settings()