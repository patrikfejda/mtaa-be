from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_model import AppBaseModel
from .message import Message
from .user import User


class Conversation(AppBaseModel):
    id: int
    synchronization_key: UUID
    name: str
    is_group: bool
    created_at: datetime

    author: User
    users: list[User]
    messages: list[Message]


class ConversationCreate(AppBaseModel):
    synchronization_key: UUID
    name: Optional[str] = Field(min_length=1)
    is_group: bool
    user_ids: set[int]
