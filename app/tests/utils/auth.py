from datetime import timedelta

from fastapi.testclient import TestClient

from app import models
from app.auth.jwt_token import create_access_token


def auth_token_and_headers(client: TestClient, username: str, password: str):
    response = client.post("v2/auth/login", json={"username": username, "password": password})
    response_payload = response.json()
    access_token = response_payload["accessToken"]
    return access_token, {"Authorization": f"Bearer {access_token}"}


def get_expired_auth_token(user: models.User):
    return create_access_token(user.username, timedelta(minutes=-1))
