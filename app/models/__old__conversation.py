from fastapi import HTTPException

from app.db.orm import session
from app.models.classes import Conversation, User


def conversationCreate(name, userIds, isGroup):
    if not isGroup and len(userIds) != 2:
        raise HTTPException(400, "Direct conversation must have exactly 2 users")
    if isGroup and len(userIds) < 2:
        raise HTTPException(400, "Group conversation must have at least 2 users")

    conversation = Conversation(name=name, isGroup=isGroup)
    session.add(conversation)

    for userId in userIds:
        user = session.query(User).filter(User.id == userId).first()
        if user is None:
            raise HTTPException(404, f"User with id {userId} not found")
        conversation.users.append(user)
    session.commit()
    return conversation


def verifyUserInConversation(userId, conversationId):
    conversation = session.query(Conversation).filter(Conversation.id == conversationId).first()
    if conversation is None:
        raise HTTPException(404, f"Conversation with id {conversationId} not found")
    for user in conversation.users:
        if str(user.id) == userId:
            return True
    raise HTTPException(
        403,
        f"User with id {userId} does not have access to conversation with id {conversationId}",
    )


def conversationGet(conversationId):
    conversation = session.query(Conversation).filter(Conversation.id == conversationId).first()
    if conversation is None:
        raise HTTPException(404, f"Conversation with id {conversationId} not found")
    return conversation


def conversationsGetAll(userId):
    user = session.query(User).filter(User.id == userId).first()
    if user is None:
        raise HTTPException(404, f"User with id {userId} not found")
    return [conversation for conversation in user.conversations]