import json

import pytest
from faker import Faker
from fastapi import WebSocketDisconnect, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models, schemas
from app.config import settings
from app.tests.utils.conversation import create_random_conversation
from app.tests.utils.message import create_random_message
from app.tests.utils.user import create_random_users

MODULE_API_PREFIX = f"{settings.API_PREFIX}/conversations"


def test_get_all_user_conversations(
    client: TestClient,
    user: models.User,
    user_auth_headers: dict[str, str],
    test_db: Session,
    faker: Faker,
):
    url = f"{MODULE_API_PREFIX}/"
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


def test_conversations_websocket_authentication(client: TestClient):
    invalid_token_url = f"{MODULE_API_PREFIX}/ws?token=HELLO"
    empty_token_url = f"{MODULE_API_PREFIX}/ws"

    with pytest.raises(WebSocketDisconnect) as invalid_token_exception:
        with client.websocket_connect(invalid_token_url):
            pass
    with pytest.raises(WebSocketDisconnect) as empty_token_exception:
        with client.websocket_connect(empty_token_url):
            pass

    assert invalid_token_exception.value.code == status.WS_1008_POLICY_VIOLATION
    assert empty_token_exception.value.code == status.WS_1008_POLICY_VIOLATION


def test_conversations_websocket_connection(client: TestClient, user_auth_token: str):
    url = f"{MODULE_API_PREFIX}/ws?token={user_auth_token}"

    try:
        with client.websocket_connect(url):
            pass
    except WebSocketDisconnect:
        pytest.fail("The websocket connection raised an exception")
    except Exception:
        pytest.fail("The websocket connection wasn't successful")
