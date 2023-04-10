from faker import Faker
from sqlalchemy.orm import Session

from app import crud, schemas
from app.config import settings


def get_test_user(test_db: Session):
    return crud.get_user_by_username(db=test_db, username=settings.TEST_USER_USERNAME)


def create_random_user(test_db: Session, faker: Faker):
    user_create = schemas.UserCreate(
        username=faker.user_name(), email=faker.email(), password=faker.password()
    )
    return crud.create_user(db=test_db, user=user_create)
