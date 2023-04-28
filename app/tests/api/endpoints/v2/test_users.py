import json

from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models, schemas
from app.config import settings
from app.tests.utils.conversation import create_random_conversation
from app.tests.utils.file import get_file_and_extension
from app.tests.utils.message import create_random_message
from app.tests.utils.user import create_random_user, create_random_users

MODULE_API_PREFIX = f"{settings.API_PREFIX}/users"


def test_get_all_users(
    client: TestClient, user_auth_headers: dict[str, str], test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}/"
    created_user = create_random_user(test_db=test_db, faker=faker)
    created_user_dict = schemas.User.from_orm(created_user).dict(by_alias=True)

    response = client.get(url, headers=user_auth_headers)
    response_payload = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(response_payload) >= 1
    assert created_user_dict in response_payload
    assert "hashedPassword" not in response_payload[0]


def test_update_users_me(client: TestClient, user_auth_headers: dict[str, str], faker: Faker):
    url = f"{MODULE_API_PREFIX}/me"
    image_file, image_file_extension = get_file_and_extension("test_image.jpg")
    form_data_payload = {"displayName": faker.first_name()}
    form_data_file_payload = {"profilePhoto": image_file}

    response = client.put(
        url, data=form_data_payload, files=form_data_file_payload, headers=user_auth_headers
    )
    response_payload = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "displayName" in response_payload
    assert "profilePhotoUrl" in response_payload
    assert response_payload["displayName"] == form_data_payload["displayName"]
    assert image_file_extension in response_payload["profilePhotoUrl"]


def test_update_users_me_wrong_file(client: TestClient, user_auth_headers: dict[str, str]):
    url = f"{MODULE_API_PREFIX}/me"
    fake_image_file, _ = get_file_and_extension("test_fake_image.jpg")
    form_data_file_payload = {"profilePhoto": fake_image_file}

    response = client.put(url, files=form_data_file_payload, headers=user_auth_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_all_current_user_conversations(
    client: TestClient,
    user: models.User,
    user_auth_headers: dict[str, str],
    test_db: Session,
    faker: Faker,
):
    url = f"{MODULE_API_PREFIX}/me/conversations"
    other_user, different_conversation_user = create_random_users(
        test_db=test_db, faker=faker, num_of_users=2
    )
    my_conversation = create_random_conversation(
        test_db=test_db, faker=faker, user_ids=[user.id, other_user.id]
    )
    created_message_json_dict = json.loads(
        schemas.Message.from_orm(
            create_random_message(
                test_db=test_db, author_id=user.id, conversation_id=my_conversation.id, faker=faker
            )
        ).json(by_alias=True)
    )
    # Create a conversation that the user is not part of
    create_random_conversation(
        test_db=test_db, faker=faker, user_ids=[other_user.id, different_conversation_user.id]
    )

    response = client.get(url, headers=user_auth_headers)
    response_payload = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(response_payload) == 1
    assert "id" in response_payload[0]
    assert "name" in response_payload[0]
    assert "createdAt" in response_payload[0]
    assert "messages" in response_payload[0]
    assert response_payload[0]["id"] == my_conversation.id
    assert response_payload[0]["name"] == my_conversation.name
    assert created_message_json_dict in response_payload[0]["messages"]
