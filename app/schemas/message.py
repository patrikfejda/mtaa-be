from datetime import datetime
from uuid import UUID

from pydantic import Field

from .base_model import AppBaseModel
from .user import User


class Message(AppBaseModel):
    id: int
    synchronization_key: UUID
    conversation_id: int
    text: str
    created_at: datetime

    author: User


class MessageCreate(AppBaseModel):
    synchronization_key: UUID
    conversation_id: int
    text: str = Field(min_length=1)
