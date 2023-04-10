from datetime import datetime

from .base_model import AppBaseModel
from .user import User


class Status(AppBaseModel):
    id: int
    latitude: str
    longitude: str
    text: str
    created_at: datetime

    author: User


class StatusCreate(AppBaseModel):
    latitude: str
    longitude: str
    text: str
