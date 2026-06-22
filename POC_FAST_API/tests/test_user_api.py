from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_user_success():
    response = client.get("/api/v1/users/10001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 10001
    assert data["first_name"] == "Promit"


def test_get_user_not_found():
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404
    assert response.json()["error_code"] == "USER_NOT_FOUND"


def test_get_user_validation_error():
    response = client.get("/api/v1/users/-1")
    assert response.status_code == 422
    assert response.json()["error_code"] == "VALIDATION_ERROR"


def test_get_users_list():
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Expect at least one known user to be present
    assert any(u.get("id") == 10001 for u in data)
