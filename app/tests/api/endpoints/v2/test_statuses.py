import json

from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models, schemas
from app.config import settings
from app.tests.utils.status import create_random_status
from app.tests.utils.user import create_random_user

MODULE_API_PREFIX = f"{settings.API_PREFIX}/statuses"


def test_get_all_statuses(
    client: TestClient,
    user_auth_headers: dict[str, str],
    user: models.User,
    test_db: Session,
    faker: Faker,
):
    url = f"{MODULE_API_PREFIX}/"
    created_status = create_random_status(test_db=test_db, author_id=user.id, faker=faker)
    created_status_json_dict = json.loads(
        schemas.Status.from_orm(created_status).json(by_alias=True)
    )

    response = client.get(url, headers=user_auth_headers)
    response_payload = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(response_payload) >= 1
    assert created_status_json_dict in response_payload
    assert "createdAt" in response_payload[0]
    assert "author" in response_payload[0]
    assert "hashedPassword" not in response_payload[0]["author"]


def test_create_status(client: TestClient, user_auth_headers: dict[str, str], faker: Faker):
    url = f"{MODULE_API_PREFIX}/"
    payload = {
        "longitude": float(faker.longitude()),
        "latitude": float(faker.latitude()),
        "text": faker.text(),
    }

    response = client.post(url, json=payload, headers=user_auth_headers)
    response_payload = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response_payload
    assert "text" in response_payload
    assert "longitude" in response_payload
    assert "latitude" in response_payload
    assert "createdAt" in response_payload
    assert "author" in response_payload
    assert response_payload["createdAt"]
    assert response_payload["author"]
    assert "hashedPassword" not in response_payload["author"]


def test_delete_status(
    client: TestClient,
    user: models.User,
    user_auth_headers: dict[str, str],
    test_db: Session,
    faker: Faker,
):
    created_status = create_random_status(test_db=test_db, author_id=user.id, faker=faker)
    url = f"{MODULE_API_PREFIX}/{created_status.id}"

    response = client.delete(url, headers=user_auth_headers)

    assert response.status_code == status.HTTP_200_OK


def test_delete_status_wrong_id(
    client: TestClient,
    user_auth_headers: dict[str, str],
    test_db: Session,
    faker: Faker,
):
    created_user = create_random_user(test_db=test_db, faker=faker)
    created_status = create_random_status(test_db=test_db, author_id=created_user.id, faker=faker)
    url = f"{MODULE_API_PREFIX}/{created_status.id}"

    # Notice the user_auth_headers (not created_user_auth_headers)
    response = client.delete(url, headers=user_auth_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
