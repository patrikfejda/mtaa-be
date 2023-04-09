from os import path

from pydantic import BaseSettings

FILESTORE_PATH = "/home/mtaa/filestore"
FILESTORE_URL = "/filestore"

ROOT_DIR = path.dirname(path.abspath(__file__))


class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    API_PREFIX = "/v2"

    JWT_SECRET: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 300
    JWT_ALGORITHM: str = "HS256"

    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int

    TEST_DATABASE_HOST: str
    TEST_DATABASE_NAME: str
    TEST_DATABASE_USER: str
    TEST_DATABASE_PASSWORD: str
    TEST_DATABASE_PORT: int

    TEST_USER_EMAIL = "example@example.com"
    TEST_USER_USERNAME = "example000"
    TEST_USER_PASSWORD = "example000"


settings = Settings()
