import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app import crud, schemas
from app.__main__ import app
from app.config import settings
from app.db.dependencies import get_db
from app.db.orm import Base
from app.tests.utils.auth import auth_headers
from app.tests.utils.user import get_test_user

engine = create_engine(
    f"postgresql://{settings.TEST_DATABASE_USER}:{settings.TEST_DATABASE_PASSWORD}@{settings.TEST_DATABASE_HOST}:{settings.TEST_DATABASE_PORT}/{settings.TEST_DATABASE_NAME}"
)
TestingSessionLocal = sessionmaker(bind=engine)


def init_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    crud.create_user(
        TestingSessionLocal(),
        user=schemas.UserCreate(
            email=settings.TEST_USER_EMAIL,
            username=settings.TEST_USER_USERNAME,
            password=settings.TEST_USER_PASSWORD,
        ),
    )


@pytest.fixture()
def test_db():
    """
    Make sure the test database is clean for each test
    Source: https://stackoverflow.com/a/67348153
    """

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(test_db: Session):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture()
def user_auth_headers(client: TestClient):
    return auth_headers(
        client=client, username=settings.TEST_USER_USERNAME, password=settings.TEST_USER_PASSWORD
    )


@pytest.fixture()
def user(test_db: Session):
    return get_test_user(test_db)


init_test_db()
