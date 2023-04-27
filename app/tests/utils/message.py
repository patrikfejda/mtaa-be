from faker import Faker
from sqlalchemy.orm import Session

from app import crud, schemas


def create_random_message(
    test_db: Session,
    author_id: int,
    conversation_id: int,
    faker: Faker,
):
    create_message = schemas.MessageCreate(
        text=faker.text(),
        conversation_id=conversation_id,
    )
    return crud.create_message(db=test_db, message=create_message, author_id=author_id)
