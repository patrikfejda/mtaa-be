from faker import Faker
from pytest import Session

from app import crud, schemas


def create_random_status(test_db: Session, author_id: int, faker: Faker):
    status_create = schemas.StatusCreate(
        text=faker.text(), longitude=faker.longitude(), latitude=faker.latitude()
    )
    return crud.create_status(db=test_db, status=status_create, author_id=author_id)
