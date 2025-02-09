import firebase_admin
from fastapi import Header
from firebase_admin import auth as firebase_auth, credentials
from settings import settings
from pydantic import BaseModel


def init() -> None:
    credential = credentials.Certificate(settings.FIREBASE_CONFIG.dict())
    firebase_admin.initialize_app(credential)


class AuthUser(BaseModel):
    name: str
    email: str
    user_id: str

    class Config:
        extra = "ignore"


def get_auth_user(authorization: str = Header(...)) -> AuthUser:
    """Get decoded token from authorization header

    Args:
        authorization: Authorization header
    Returns:
        dict: Decoded token
    """
    token = authorization.replace("Bearer ", "")
    decoded_token = firebase_auth.verify_id_token(token)
    return AuthUser(**decoded_token)
