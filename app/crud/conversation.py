from sqlalchemy.orm import Session

from app import models, schemas


def get_conversation(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()


def create_conversation(db: Session, conversation: schemas.ConversationCreate):
    db_conversation = models.Conversation(name=conversation.name, is_group=conversation.is_group)
    db_conversation.users.extend(
        db.query(models.User).filter(models.User.id.in_(conversation.user_ids)).all()
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation
