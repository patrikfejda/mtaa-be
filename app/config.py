from pydantic import BaseSettings

DONT_ALLOW_NOT_UNIQUE_EMAIL = False
DONT_ALLOW_NOT_UNIQUE_USERNAME = False

class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int

settings = Settings()
