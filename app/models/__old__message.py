from fastapi import HTTPException

from app.db.orm import session
from app.models.classes import Conversation, Message


def messageCreate(senderId: int, conversationId: int, message: str, photoUrl: str):
    new_message = Message(
        userId=senderId,
        conversationId=conversationId,
        message=message,
        photoUrl=photoUrl,
    )
    session.add(new_message)
    session.commit()
    return new_message


def messageGet(userId: int, messageId: int):
    message = session.query(Message).filter(Message.id == messageId).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    conversation = (
        session.query(Conversation).filter(Conversation.id == message.conversationId).first()
    )
    if userId not in [str(user.id) for user in conversation.users]:
        raise HTTPException(status_code=403, detail="Forbidden")

    return message


def messageConversationAll(userId: int, conversationId: int):
    conversation = session.query(Conversation).filter(Conversation.id == conversationId).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if userId not in [str(user.id) for user in conversation.users]:
        raise HTTPException(status_code=403, detail="Forbidden")

    messages = session.query(Message).filter(Message.conversationId == conversationId).all()
    return [message for message in messages]
