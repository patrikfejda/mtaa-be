from .base_model import AppBaseModel
from .user import User


class AuthLogin(AppBaseModel):
    username: str
    password: str


class AuthResponse(AppBaseModel):
    access_token: str
    user: User
