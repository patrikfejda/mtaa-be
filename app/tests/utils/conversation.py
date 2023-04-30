from faker import Faker
from sqlalchemy.orm import Session

from app import crud, schemas


def create_random_conversation(
    test_db: Session, faker: Faker, author_id: int, user_ids: set[int], is_group: bool = True
):
    conversation_create = schemas.ConversationCreate(
        synchronization_key=faker.uuid4(), name=faker.name(), is_group=is_group, user_ids=user_ids
    )
    return crud.create_conversation(
        db=test_db, conversation=conversation_create, author_id=author_id
    )
