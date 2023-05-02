import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.tests.utils.websocket import create_websocket_message, websocket_receive_json_timeouted

MODULE_API_PREFIX = f"{settings.API_PREFIX}/conversations/ws"


@pytest.mark.slow
def test_client_ping(client: TestClient, user_auth_token: str):
    url = f"{MODULE_API_PREFIX}?token={user_auth_token}"
    websocket_message = create_websocket_message(token=user_auth_token, event_name="PING", data={})

    with client.websocket_connect(url) as websocket:
        websocket.send_json(websocket_message)
        response = websocket_receive_json_timeouted(websocket)

    assert response["event"] == "PONG"
    assert response["data"] == {}
