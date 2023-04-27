import pytest
from fastapi import WebSocketDisconnect, status
from fastapi.testclient import TestClient

from app.config import settings

MODULE_API_PREFIX = f"{settings.API_PREFIX}/conversations"


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
