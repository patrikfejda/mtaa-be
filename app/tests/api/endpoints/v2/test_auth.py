from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import settings
from app.tests.utils.user import create_random_user

MODULE_API_PREFIX = f"{settings.API_PREFIX}/auth"


def test_auth_login(client: TestClient):
    url = f"{MODULE_API_PREFIX}/login"
    payload = {"username": settings.TEST_USER_USERNAME, "password": settings.TEST_USER_PASSWORD}

    response = client.post(url, json=payload)
    response_payload = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "accessToken" in response_payload
    assert "user" in response_payload
    assert response_payload["accessToken"]
    assert response_payload["user"]["username"] == payload["username"]
    assert "hashedPassword" not in response_payload["user"]


def test_auth_incorrect_login(client: TestClient):
    url = f"{MODULE_API_PREFIX}/login"
    payload = {"username": settings.TEST_USER_USERNAME, "password": "__incorrect_password__"}

    response = client.post(url, json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_auth_register(client: TestClient, faker: Faker):
    url = f"{MODULE_API_PREFIX}/register"
    payload = {
        "email": faker.email(),
        "username": faker.user_name(),
        "password": faker.password(),
    }

    response = client.post(url, json=payload)
    response_payload = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "accessToken" in response_payload
    assert "user" in response_payload
    assert response_payload["accessToken"]
    assert response_payload["user"]["username"] == payload["username"]
    assert "hashedPassword" not in response_payload["user"]


def test_auth_register_existing(client: TestClient, test_db: Session, faker: Faker):
    url = f"{MODULE_API_PREFIX}/register"
    existing_user = create_random_user(test_db=test_db, faker=faker)
    payloadExistingEmail = {
        "email": existing_user.email,
        "username": faker.user_name(),
        "password": faker.password(),
    }
    payloadExistingUsername = {
        "email": faker.email(),
        "username": existing_user.username,
        "password": faker.password(),
    }

    responseEmail = client.post(url, json=payloadExistingEmail)
    responseUsername = client.post(url, json=payloadExistingUsername)

    assert responseEmail.status_code == status.HTTP_400_BAD_REQUEST
    assert responseUsername.status_code == status.HTTP_400_BAD_REQUEST


def test_auth_register_empty(client: TestClient, faker: Faker):
    url = f"{MODULE_API_PREFIX}/register"
    payloadEmptyEmail = {
        "email": "",
        "username": faker.user_name(),
        "password": faker.password(),
    }
    payloadEmptyUsername = {
        "email": faker.email(),
        "username": "",
        "password": faker.password(),
    }
    payloadEmptyPassword = {
        "email": faker.email(),
        "username": faker.user_name(),
        "password": "",
    }

    responseEmptyEmail = client.post(url, json=payloadEmptyEmail)
    responseEmptyUsername = client.post(url, json=payloadEmptyUsername)
    responseEmptyPassword = client.post(url, json=payloadEmptyPassword)

    assert responseEmptyEmail.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert responseEmptyUsername.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert responseEmptyPassword.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_auth_check(client: TestClient, user_auth_headers: dict[str, str]):
    url = f"{MODULE_API_PREFIX}/check"

    response = client.get(url, headers=user_auth_headers)

    assert response.status_code == status.HTTP_200_OK
