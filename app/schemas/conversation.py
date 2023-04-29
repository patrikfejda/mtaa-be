from datetime import datetime
from typing import Optional

from pydantic import Field

from .base_model import AppBaseModel
from .message import Message
from .user import User


class Conversation(AppBaseModel):
    id: int
    name: str
    is_group: bool
    created_at: datetime

    users: list[User]
    messages: list[Message]


class ConversationCreate(AppBaseModel):
    name: Optional[str] = Field(min_length=1)
    is_group: bool
    user_ids: set[int]
