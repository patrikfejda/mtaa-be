from fastapi.testclient import TestClient


def auth_headers(client: TestClient, username: str, password: str):
    response = client.post("v2/auth/login", json={"username": username, "password": password})
    response_payload = response.json()
    access_token = response_payload["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}
