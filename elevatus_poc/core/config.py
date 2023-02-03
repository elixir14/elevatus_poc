from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DEBUG: bool = True
    MONGODB_URL: str
    DATABASE_NAME: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
