from datetime import datetime
from typing import Optional

from pydantic import Field

from .base_model import AppBaseModel
from .message import Message


class Conversation(AppBaseModel):
    id: int
    name: str
    is_group: bool
    created_at: datetime

    messages: list[Message]


class ConversationCreate(AppBaseModel):
    name: Optional[str] = Field(min_length=1)
    is_group: bool
    user_ids: set[int]
