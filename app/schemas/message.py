from datetime import datetime

from pydantic import Field

from .base_model import AppBaseModel
from .user import User


class Message(AppBaseModel):
    id: int
    conversation_id: int
    text: str
    created_at: datetime

    author: User


class MessageCreate(AppBaseModel):
    conversation_id: int
    text: str = Field(min_length=1)
