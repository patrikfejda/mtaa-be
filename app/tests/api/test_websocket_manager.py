import pytest
from faker import Faker
from fastapi import WebSocketDisconnect, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.tests.utils.auth import get_expired_auth_token
from app.tests.utils.user import create_random_user
from app.tests.utils.websocket import create_websocket_message, websocket_receive_json_timeouted

MODULE_API_PREFIX = f"{settings.API_PREFIX}/conversations/ws"


def test_no_bytes_websocket_message(client: TestClient, user_auth_token: str):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_bytes(b"hello")
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


def test_no_text_websocket_message(client: TestClient, user_auth_token: str):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_text("hello")
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


def test_json_websocket_message_parser_no_format(client: TestClient, user_auth_token: str):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    websocket_message = {"invalid_key": "invalid_value"}

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


def test_json_websocket_message_parser_no_token(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    other_user = create_random_user(test_db=test_db, faker=faker)
    payload = {"isGroup": False, "userIds": [user.id, other_user.id]}
    websocket_message = {"event": "CREATE_CONVERSATION", "data": payload}

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


def test_json_websocket_message_parser_wrong_event(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    other_user = create_random_user(test_db=test_db, faker=faker)
    payload = {"isGroup": False, "userIds": [user.id, other_user.id]}
    websocket_message = create_websocket_message(
        token=user_auth_token, event_name="NONEXISTENT_EVENT", data=payload
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


def test_json_websocket_message_parser_wrong_data(client: TestClient, user_auth_token: str):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    websocket_message = create_websocket_message(
        token=user_auth_token, event_name="CREATE_CONVERSATION", data="not object"
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


def test_auth_token_expiration(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    expired_auth_token = get_expired_auth_token(user)
    other_user = create_random_user(test_db=test_db, faker=faker)
    websocket_message = create_websocket_message(
        token=expired_auth_token,
        event_name="CREATE_CONVERSATION",
        data={"isGroup": False, "userIds": [user.id, other_user.id]},
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1008_POLICY_VIOLATION
