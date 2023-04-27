from typing import List

from sqlalchemy import DECIMAL, Boolean, Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import Mapped, relationship

from app.db.orm import Base

conversations_users = Table(
    "conversations_users",
    Base.metadata,
    Column("conversation_id", ForeignKey("conversations.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    display_name = Column(String)
    profile_photo_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversations: Mapped[List["Conversation"]] = relationship(
        secondary=conversations_users, back_populates="users"
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_group = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users: Mapped[List["User"]] = relationship(
        secondary=conversations_users, back_populates="conversations"
    )
    messages: Mapped[List["Message"]] = relationship()


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    latitude = Column(DECIMAL(8, 6))
    longitude = Column(DECIMAL(9, 6))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    author: Mapped["User"] = relationship()


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    text = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    author: Mapped["User"] = relationship()
