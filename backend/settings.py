import logging
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from enums import Environment

logger = logging.getLogger(__name__)

load_dotenv()


class Settings(BaseSettings):
    ROOT_DIR_NAME: str = os.path.basename(os.path.abspath(os.curdir))
    MONGODB_CONNECTION_STRING: str = "mongodb://localhost:27017"
    DEBUG: bool = False
    RELOAD: bool = False
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
    ]

    class Config:
        env_file = ".env"


class DevelopmentSettings(Settings):
    DATABASE_NAME: str = "development"
    MONGODB_CONNECTION_STRING: str = f"mongodb://localhost:27017/{DATABASE_NAME}"
    RELOAD: bool = True
    HOST: str = "localhost"
    PORT: int = 8000


class TestSettings(Settings):
    DATABASE_NAME: str = "testing"
    MONGODB_CONNECTION_STRING: str = f"mongodb://0.0.0.0:27017/{DATABASE_NAME}"


def get_settings() -> Settings:
    environment = os.getenv("ENVIRONMENT").lower()
    env_settings = {
        Environment.DEVELOPMENT.value: DevelopmentSettings,
        Environment.TESTING.value: TestSettings,
    }
    return env_settings[environment]()


settings = get_settings()
