from contextlib import ExitStack

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
    get_users_tokens,
)
from app.tests.utils.websocket import create_websocket_message, websocket_receive_json_timeouted

MODULE_API_PREFIX = f"{settings.API_PREFIX}/conversations/ws"


@pytest.mark.slow
def test_create_direct_conversation(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    user_url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    new_user, new_user_token = create_random_user_with_token(test_db=test_db, faker=faker)
    new_user_url = f"{MODULE_API_PREFIX}?token={new_user_token}"
    payload = {
        "synchronizationKey": faker.uuid4(),
        "isGroup": False,
        "userIds": [user.id, new_user.id],
    }
    websocket_message = create_websocket_message(
        token=user_auth_token,
        event_name="CREATE_CONVERSATION",
        data=payload,
    )

    with (
        client.websocket_connect(user_url) as user_websocket,
        client.websocket_connect(new_user_url) as new_user_websocket,
    ):
        user_websocket.send_json(websocket_message)
        user_response = websocket_receive_json_timeouted(user_websocket)
        new_user_response = websocket_receive_json_timeouted(new_user_websocket)

    assert user_response != None
    assert new_user_response != None
    assert "token" not in new_user_response
    assert "event" in new_user_response
    assert new_user_response["event"] == "NEW_CONVERSATION"
    assert "data" in new_user_response
    assert "id" in new_user_response["data"]
    assert "synchronizationKey" in new_user_response["data"]
    assert "name" in new_user_response["data"]
    assert "isGroup" in new_user_response["data"]
    assert "createdAt" in new_user_response["data"]
    assert "messages" in new_user_response["data"]
    assert new_user_response["data"]["synchronizationKey"] == payload["synchronizationKey"]
    assert new_user_response["data"]["name"] == (new_user.display_name or new_user.username)
    assert new_user_response["data"]["isGroup"] == False
    assert new_user_response["data"]["messages"] == []


@pytest.mark.slow
def test_create_direct_conversation_already_exists(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    new_user = create_random_user(test_db=test_db, faker=faker)
    create_random_conversation(
        test_db=test_db,
        faker=faker,
        author_id=user.id,
        is_group=False,
        user_ids=[user.id, new_user.id],
    )
    payload = {
        "synchronizationKey": faker.uuid4(),
        "isGroup": False,
        "userIds": [new_user.id, user.id],
    }
    websocket_message = create_websocket_message(
        token=user_auth_token,
        event_name="CREATE_CONVERSATION",
        data=payload,
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


@pytest.mark.slow
def test_create_direct_conversation_many_ids(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    users = create_random_users(test_db=test_db, faker=faker, num_of_users=3)
    users_ids = list(map(lambda user: user.id, users))
    payload = {
        "synchronizationKey": faker.uuid4(),
        "isGroup": False,
        "userIds": [user.id, *users_ids],
    }
    websocket_message = create_websocket_message(
        token=user_auth_token,
        event_name="CREATE_CONVERSATION",
        data=payload,
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


@pytest.mark.slow
def test_create_direct_conversation_no_creator_id(
    client: TestClient, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    users = create_random_users(test_db=test_db, faker=faker, num_of_users=2)
    payload = {
        "synchronizationKey": faker.uuid4(),
        "isGroup": False,
        "userIds": [users[0].id, users[1].id],
    }
    websocket_message = create_websocket_message(
        token=user_auth_token,
        event_name="CREATE_CONVERSATION",
        data=payload,
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


@pytest.mark.slow
def test_create_group_conversation(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    user_url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    other_users = create_random_users(test_db=test_db, faker=faker, num_of_users=5)
    other_users_ids = list(map(lambda other_user: other_user.id, other_users))
    other_users_urls = list(
        map(lambda token: f"{MODULE_API_PREFIX}?token={token}", get_users_tokens(other_users))
    )
    payload = {
        "synchronizationKey": faker.uuid4(),
        "name": faker.name(),
        "isGroup": True,
        "userIds": [user.id, *other_users_ids],
    }
    websocket_message = create_websocket_message(
        token=user_auth_token,
        event_name="CREATE_CONVERSATION",
        data=payload,
    )

    users_responses = []
    with ExitStack() as stack:
        user_websocket = stack.enter_context(client.websocket_connect(user_url))
        other_users_websockets = [
            stack.enter_context(client.websocket_connect(url)) for url in other_users_urls
        ]
        user_websocket.send_json(websocket_message)
        user_response = websocket_receive_json_timeouted(user_websocket)
        users_responses.append(user_response)
        for other_user_websocket in other_users_websockets:
            other_user_response = websocket_receive_json_timeouted(other_user_websocket)
            if other_user_response:
                users_responses.append(other_user_response)

    assert user_response != None
    assert len(users_responses) == len(other_users) + 1
    for user_response in users_responses:
        assert "token" not in user_response
        assert "event" in user_response
        assert user_response["event"] == "NEW_CONVERSATION"
        assert "data" in user_response
        assert user_response["data"]["name"] == payload["name"]
        assert user_response["data"]["isGroup"] == True
        assert user_response["data"]["messages"] == []


@pytest.mark.slow
def test_create_group_conversation_missing_name(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    users = create_random_users(test_db=test_db, faker=faker, num_of_users=3)
    users_ids = list(map(lambda user: user.id, users))
    payload = {
        "synchronizationKey": faker.uuid4(),
        "isGroup": True,
        "userIds": [user.id, *users_ids],
    }
    websocket_message = create_websocket_message(
        token=user_auth_token,
        event_name="CREATE_CONVERSATION",
        data=payload,
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


@pytest.mark.slow
def test_create_group_conversation_wrong_synchronization_key(
    client: TestClient, user: models.User, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    users = create_random_users(test_db=test_db, faker=faker, num_of_users=3)
    users_ids = list(map(lambda user: user.id, users))
    payload = {
        "synchronizationKey": "invalid_key",
        "name": faker.name(),
        "isGroup": True,
        "userIds": [user.id, *users_ids],
    }
    websocket_message = create_websocket_message(
        token=user_auth_token,
        event_name="CREATE_CONVERSATION",
        data=payload,
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA


@pytest.mark.slow
def test_create_group_conversation_no_creator_id(
    client: TestClient, user_auth_token: str, test_db: Session, faker: Faker
):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    users = create_random_users(test_db=test_db, faker=faker, num_of_users=3)
    users_ids = list(map(lambda user: user.id, users))
    payload = {
        "synchronizationKey": faker.uuid4(),
        "name": faker.name(),
        "isGroup": True,
        "userIds": users_ids,
    }
    websocket_message = create_websocket_message(
        token=user_auth_token,
        event_name="CREATE_CONVERSATION",
        data=payload,
    )

    with pytest.raises(WebSocketDisconnect) as exception:
        with client.websocket_connect(url) as websocket:
            websocket.send_json(websocket_message)
            websocket_receive_json_timeouted(websocket)

    assert exception.value.code == status.WS_1003_UNSUPPORTED_DATA
