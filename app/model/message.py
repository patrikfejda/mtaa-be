from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime, func
from app.db.orm import session, engine
from fastapi import HTTPException
from app.support.jwt import generate_jwt
from app.config import DONT_ALLOW_NOT_UNIQUE_EMAIL, DONT_ALLOW_NOT_UNIQUE_USERNAME
from app.model.classes import Message, User, Conversation


Base = declarative_base()

def messageCreate(
    sender_id: int,
    conversation_id: int,
    message: str,
    photo_url: str
):
    new_message = Message(
        user_id=sender_id,
        conversation_id=conversation_id,
        message=message,
        photo_url=photo_url
    )
    session.add(new_message)
    session.commit()
    return new_message.public_data()

def messageGet(user_id: int, id: int):
    message = session.query(Message).filter(Message.id == id).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if user_id not in [user.id for user in message.conversation.users]:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return message.public_data()

def messageConversationAll(user_id: int, conversation_id: int):
    conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if user_id not in [user.id for user in conversation.users]:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    messages = session.query(Message).filter(Message.conversation_id == conversation_id).all()
    return [message.public_data() for message in messages]
    