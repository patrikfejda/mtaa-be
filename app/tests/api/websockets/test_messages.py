import pytest
from faker import Faker
from fastapi import WebSocketDisconnect, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.tests.utils.conversation import create_random_conversation
from app.tests.utils.user import (
    create_random_user,
    create_random_user_with_token,
    create_random_users,
)
from app.tests.utils.websocket import create_websocket_message, websocket_receive_json_timeouted

MODULE_API_PREFIX = f"{settings.API_PREFIX}/conversations/ws"


@pytest.mark.slow
def test_create_message(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    user_url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    conversation_user, conversation_user_token = create_random_user_with_token(
        test_db=test_db, faker=faker
    )
    _, different_user_token = create_random_user_with_token(test_db=test_db, faker=faker)
    conversation_user_url = f"{MODULE_API_PREFIX}?token={conversation_user_token}"
    different_user_url = f"{MODULE_API_PREFIX}?token={different_user_token}"
    conversation = create_random_conversation(
        test_db=test_db, faker=faker, user_ids=[user.id, conversation_user.id]
    )
    payload = {"conversationId": conversation.id, "text": faker.text()}
    websocket_message = create_websocket_message(
        token=user_auth_token, event_name="CREATE_MESSAGE", data=payload
    )

    with (
        client.websocket_connect(user_url) as user_websocket,
        client.websocket_connect(conversation_user_url) as conversation_user_websocket,
        client.websocket_connect(different_user_url) as different_user_websocket,
    ):
        user_websocket.send_json(websocket_message)
        user_response = websocket_receive_json_timeouted(user_websocket)
        conversation_user_response = websocket_receive_json_timeouted(conversation_user_websocket)
        different_user_response = websocket_receive_json_timeouted(different_user_websocket)

    assert user_response == None
    assert different_user_response == None
    assert conversation_user_response != None
    assert "token" not in conversation_user_response
    assert "event" in conversation_user_response
    assert conversation_user_response["event"] == "NEW_MESSAGE"
    assert "data" in conversation_user_response
    assert "conversationId" in conversation_user_response["data"]
    assert "text" in conversation_user_response["data"]
    assert "createdAt" in conversation_user_response["data"]
    assert "author" in conversation_user_response["data"]
    assert conversation_user_response["data"]["conversationId"] == payload["conversationId"]
    assert conversation_user_response["data"]["text"] == payload["text"]
    assert "id" in conversation_user_response["data"]["author"]
    assert conversation_user_response["data"]["author"]["id"] == user.id


@pytest.mark.slow
def test_create_message_user_not_in_conversation(
    client: TestClient, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    users = create_random_users(test_db=test_db, faker=faker, num_of_users=2)
    users_ids = list(map(lambda user: user.id, users))
    conversation = create_random_conversation(test_db=test_db, faker=faker, user_ids=users_ids)
    payload = {"conversationId": conversation.id, "text": faker.text()}
    websocket_message = create_websocket_message(
        token=user_auth_token, event_name="CREATE_MESSAGE", data=payload
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


@pytest.mark.slow
def test_create_message_nonexistent_id(client: TestClient, user_auth_token: str, faker: Faker):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    payload = {"conversationId": 1234, "text": faker.text()}
    websocket_message = create_websocket_message(
        token=user_auth_token, event_name="CREATE_MESSAGE", data=payload
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


@pytest.mark.slow
def test_create_message_empty_text(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    conversation_user = create_random_user(test_db=test_db, faker=faker)
    conversation = create_random_conversation(
        test_db=test_db, faker=faker, user_ids=[user.id, conversation_user.id]
    )
    payload = {"conversationId": conversation.id, "text": ""}
    websocket_message = create_websocket_message(
        token=user_auth_token, event_name="CREATE_MESSAGE", data=payload
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA
