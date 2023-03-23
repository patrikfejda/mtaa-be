from app.db.orm import session
from fastapi import HTTPException
from app.support.jwt import generate_jwt
from app.config import DONT_ALLOW_NOT_UNIQUE_EMAIL, DONT_ALLOW_NOT_UNIQUE_USERNAME
from app.model.classes import Conversation, User



def conversationCreate(name, user_ids, is_group):
    if not is_group and len(user_ids) != 2:
        raise HTTPException(400, "Direct conversation must have exactly 2 users")
    if is_group and len(user_ids) < 2:
        raise HTTPException(400, "Group conversation must have at least 2 users")

    conversation = Conversation(name=name, is_group=is_group)
    session.add(conversation)
    
    for user_id in user_ids:
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(404, f"User with id {user_id} not found")
        conversation.users.append(user)
    session.commit()
    return conversation.private_data()

def verifyUserInConversation(user_id, conversation_id):
    conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(404, f"Conversation with id {conversation_id} not found")
    for user in conversation.users:
        if str(user.id) == user_id:
            return True
    raise HTTPException(403, f"User with id {user_id} does not have access to conversation with id {conversation_id}")

def conversationGet(conversation_id):
    conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(404, f"Conversation with id {conversation_id} not found")
    return conversation.private_data()

def conversationsGetAll(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(404, f"User with id {user_id} not found")
    return [conversation.private_data() for conversation in user.conversations]