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


from app.model.user import User
Column(Integer, Sequence("conversation_id_seq"), primary_key=True)

Base = declarative_base()

association_table = Table(
    "association_table",
    Base.metadata,
    Column("conversation_id", ForeignKey("conversations.id")),
    Column("user_id", ForeignKey("users.id")),
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

def create_table():
    print("Creating table conversation")
    Base.metadata.create_all(engine)

# User(name='ed', fullname='Ed Jones', nickname='edsnickname')

# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()
# ed_user = User(email="patrikfejda@gmail.com", username="patrikfejda", display_name="Patrik Fejda")
# session.add(ed_user)
