from sqlalchemy.orm import Session

from app import crud, schemas
from app.config import settings
from app.db.orm import Base, engine


def init_db(db: Session):
    Base.metadata.create_all(bind=engine)

    user = crud.get_user_by_username(db, username=settings.TEST_USER_USERNAME)
    if not user:
        user_create = schemas.UserCreate(
            email=settings.TEST_USER_EMAIL,
            username=settings.TEST_USER_USERNAME,
            password=settings.TEST_USER_PASSWORD,
        )
        user = crud.create_user(db, user=user_create)
