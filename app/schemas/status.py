from datetime import datetime

from pydantic import Field

from .base_model import AppBaseModel
from .user import User


class Status(AppBaseModel):
    id: int
    latitude: str
    longitude: str
    text: str
    created_at: datetime

    author: User


# TODO shouldn't latitude, longitude be floats?
class StatusCreate(AppBaseModel):
    latitude: str
    longitude: str
    text: str = Field(min_length=1)
