import os
from pydantic import BaseModel
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from enums import Environment


load_dotenv()


class FirebaseConfig(BaseModel):
    type: str = "service_account"
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    client_x509_cert_url: str
    auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    token_uri: str = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
    universe_domain: str = "googleapis.com"


class Settings(BaseSettings):
    ROOT_DIR_NAME: str = os.path.basename(os.path.abspath(os.curdir))
    DEBUG: bool = False
    RELOAD: bool = False
    ALLOWED_ORIGINS: list[str] = []

    class Config:
        env_file = ".env"
        extra = "allow"


class DevelopmentSettings(Settings):
    DATABASE_NAME: str = "development"
    RELOAD: bool = True
    MONGODB_CONNECTION_STRING: str = os.getenv(
        "MONGODB_CONNECTION_STRING", f"mongodb://localhost:27017/{DATABASE_NAME}"
    )
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = os.getenv("PORT", 8000)
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", ["http://localhost:3000"])
    FIREBASE_CONFIG: FirebaseConfig = FirebaseConfig(
        project_id=os.getenv("FIREBASE_PROJECT_ID", "development"),
        private_key_id=os.getenv("FIREBASE_PRIVATE_KEY_ID", "private_key_id"),
        private_key=os.getenv("FIREBASE_PRIVATE_KEY", "private_key"),
        client_email=os.getenv("FIREBASE_CLIENT_EMAIL", "client_email"),
        client_id=os.getenv("FIREBASE_CLIENT_ID", "client_id"),
        client_x509_cert_url=os.getenv(
            "FIREBASE_CLIENT_X509_CERT_URL", "client_x509_cert_url"
        ),
    )


class TestSettings(Settings):
    DATABASE_NAME: str = "testing"
    MONGODB_CONNECTION_STRING: str = f"mongodb://0.0.0.0:27017/{DATABASE_NAME}"
    FIREBASE_CONFIG: FirebaseConfig = FirebaseConfig(
        project_id="test_project_id",
        private_key_id="test_private_key_id",
        private_key="test_private_key",
        client_email="test_client_email",
        client_id="test_client_id",
        client_x509_cert_url="test_client_x509_cert_url",
    )


def _get_settings() -> Settings:
    environment = os.getenv("ENVIRONMENT").lower()
    env_settings = {
        Environment.DEVELOPMENT.value: DevelopmentSettings,
        Environment.TESTING.value: TestSettings,
    }
    return env_settings[environment]()


settings = _get_settings()


__all__ = ["settings"]
