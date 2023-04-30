from sqlalchemy.orm import Session

from app import models, schemas


def get_conversation(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()


def create_conversation(db: Session, conversation: schemas.ConversationCreate, author_id: int):
    db_conversation = models.Conversation(
        synchronization_key=conversation.synchronization_key,
        name=conversation.name,
        is_group=conversation.is_group,
        author_id=author_id,
    )
    db_conversation.users.extend(
        db.query(models.User).filter(models.User.id.in_(conversation.user_ids)).all()
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation
