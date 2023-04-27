from faker import Faker
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.auth.jwt_token import create_access_token
from app.config import settings


def get_test_user(test_db: Session):
    return crud.get_user_by_username(db=test_db, username=settings.TEST_USER_USERNAME)


def create_random_user(test_db: Session, faker: Faker):
    user_create = schemas.UserCreate(
        username=faker.user_name(), email=faker.email(), password=faker.password()
    )
    return crud.create_user(db=test_db, user=user_create)


def create_random_user_with_token(test_db: Session, faker: Faker):
    new_user = create_random_user(test_db=test_db, faker=faker)
    return new_user, create_access_token(new_user.username)


def create_random_users(test_db: Session, faker: Faker, num_of_users: int):
    return [create_random_user(test_db=test_db, faker=faker) for _ in range(num_of_users)]


def get_users_tokens(users: list[models.User]):
    return map(lambda user: create_access_token(user.username), users)
