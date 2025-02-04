import logging
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from enums import Environment

logger = logging.getLogger(__name__)

load_dotenv()


class Settings(BaseSettings):
    ROOT_DIR_NAME: str = os.path.basename(os.path.abspath(os.curdir))
    DEBUG: bool = False
    RELOAD: bool = False
    ALLOWED_ORIGINS: list[str] = []

    class Config:
        env_file = ".env"


class DevelopmentSettings(Settings):
    DATABASE_NAME: str = "development"
    RELOAD: bool = True
    MONGODB_CONNECTION_STRING: str = os.getenv(
        "MONGODB_CONNECTION_STRING", f"mongodb://localhost:27017/{DATABASE_NAME}"
    )
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = os.getenv("PORT", 8000)
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", ["http://localhost:3000"])


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
