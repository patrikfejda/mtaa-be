from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime, func, Boolean
from app.db.orm import session, engine
from fastapi import HTTPException
from app.support.jwt import generate_jwt
from app.config import DONT_ALLOW_NOT_UNIQUE_EMAIL, DONT_ALLOW_NOT_UNIQUE_USERNAME
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from typing import List

Column(Integer, Sequence("conversationId_seq"), primary_key=True)
Column(Integer, Sequence("user_id_seq"), primary_key=True)
Column(Integer, Sequence("message_id_seq"), primary_key=True)
Column(Integer, Sequence("status_id_seq"), primary_key=True)

Base = declarative_base()

association_table = Table(
    "association_table",
    Base.metadata,
    Column("conversationId", ForeignKey("conversations.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    jwt = Column(String)
    displayName = Column(String)
    profilePhotoUrl = Column(String)
    conversations: Mapped[List["Conversation"]] = relationship(
        secondary=association_table, back_populates="users"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def public_data(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "displayName": self.displayName,
            "profilePhotoUrl": self.profilePhotoUrl,
            "created_at": self.created_at,
        }

    def private_data(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "displayName": self.displayName,
            "profilePhotoUrl": self.profilePhotoUrl,
            "created_at": self.created_at,
            "conversations": self.conversations,
        }

    def __repr__(self):
        return (
            "<User(id='%s', email='%s', username='%s', displayName='%s', profilePhotoUrl='%s', created_at='%s')>"
            % (
                self.id,
                self.email,
                self.username,
                self.displayName,
                self.profilePhotoUrl,
                self.created_at,
            )
        )


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    isGroup = Column(Boolean)
    name = Column(String)
    users: Mapped[List["User"]] = relationship(
        secondary=association_table, back_populates="conversations"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Conversation(id='%s', isGroup='%s', name='%s', created_at='%s, users='%s')>" % (
            self.id,
            self.isGroup,
            self.name,
            self.created_at,
            [x.public_data() for x in self.users]
        )
    
    def private_data(self):
        return {
            "id": self.id,
            "isGroup": self.isGroup,
            "name": self.name,
            "created_at": self.created_at,
            "users": [x.public_data() for x in self.users]
        }


class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Status(id='%s', user_id='%s', status='%s', latitude='%s', longitude='%s', created_at='%s')>" % (
            self.id,
            self.user_id,
            self.status,
            self.latitude,
            self.longitude,
            self.created_at,
        )

    def public_data(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": self.created_at,
        }
    
    def private_data(self):
        return self.public_data()
    

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    conversationId = Column(Integer, ForeignKey("conversations.id"))
    message = Column(String)
    photo_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Message(id='%s', user_id='%s', conversationId='%s', message='%s', photo_url='%s', created_at='%s')>" % (
            self.id,
            self.user_id,
            self.conversationId,
            self.message,
            self.photo_url,
            self.created_at,
        )

    def public_data(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "conversationId": self.conversationId,
            "message": self.message,
            "photo_url": self.photo_url,
            "created_at": self.created_at,
        }


    def private_data(self):
        return self.public_data()

def create_tables():
    print("Creating DB tables")
    Base.metadata.create_all(engine)





    # user = User(email="a", username="a", displayName="a")
    # session.add(user)
    # user2 = User(email="b", username="b", displayName="b")
    # session.add(user2)

    # conversation = Conversation(isGroup=False, name="a")
    # session.add(conversation)
    # conversation2 = Conversation(isGroup=False, name="b")
    # session.add(conversation2)

    # conversation.users.append(user)
    # conversation.users.append(user2)
    # conversation2.users.append(user)
    # conversation2.users.append(user2)
    # session.commit()