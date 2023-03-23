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
Column(Integer, Sequence("conversation_id_seq"), primary_key=True)

Base = declarative_base()

association_table = Table(
    "association_table",
    Base.metadata,
    Column("conversation_id", ForeignKey("conversations.id")),
    Column("user_id", ForeignKey("users.id")),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    jwt = Column(String)
    display_name = Column(String)
    profile_photo_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_safe_data(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "display_name": self.display_name,
            "profile_photo_url": self.profile_photo_url,
            "created_at": self.created_at,
        }

    def __repr__(self):
        return (
            "<User(id='%s', email='%s', username='%s', display_name='%s', profile_photo_url='%s', created_at='%s')>"
            % (
                self.id,
                self.email,
                self.username,
                self.display_name,
                self.profile_photo_url,
                self.created_at,
            )
        )

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    is_group = Column(Boolean)
    name = Column(String)
    users: Mapped[List[User]] = relationship(secondary=association_table)
    created_at = Column(String)

    def __repr__(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "display_name": self.display_name,
            "profile_photo_url": self.profile_photo_url,
            "created_at": self.created_at
        }

def create_tables():
    print("Creating DB tables")
    Base.metadata.create_all(engine)

    # user = User(email="a", username="a", display_name="a")
    # session.add(user)
    # user2 = User(email="b", username="b", display_name="b")
    # session.add(user2)
    
    # conversation = Conversation(is_group=False, name="a")
    # session.add(conversation)
    # conversation2 = Conversation(is_group=False, name="b")
    # session.add(conversation2)
    
    # conversation.users.append(user)
    # conversation.users.append(user2)
    # conversation2.users.append(user)
    # conversation2.users.append(user2)
    # session.commit()


