from typing import List

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Sequence,
    String,
    Table,
    func,
)
from sqlalchemy.orm import Mapped, relationship

from app.db.orm import Base

# TODO what is this?
Column(Integer, Sequence("conversationId_seq"), primary_key=True)
Column(Integer, Sequence("userId_seq"), primary_key=True)
Column(Integer, Sequence("messageId_seq"), primary_key=True)
Column(Integer, Sequence("statusId_seq"), primary_key=True)

conversation_user = Table(
    "conversation_user",
    Base.metadata,
    Column("conversationId", ForeignKey("conversations.id"), primary_key=True),
    Column("userId", ForeignKey("users.id"), primary_key=True),
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
        secondary=conversation_user, back_populates="users"
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    isGroup = Column(Boolean)
    name = Column(String)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())

    users: Mapped[List["User"]] = relationship(
        secondary=conversation_user, back_populates="conversations"
    )


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    latitude = Column(DECIMAL(8, 6))
    longitude = Column(DECIMAL(9, 6))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    author = relationship("User")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("users.id"))
    conversationId = Column(Integer, ForeignKey("conversations.id"))
    message = Column(String)
    photoUrl = Column(String)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
