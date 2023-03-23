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


