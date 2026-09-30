from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_openapi():

    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert "paths" in data

    assert "/qa" in data["paths"]

    assert "/explain" in data["paths"]

    assert "/quiz" in data["paths"]

    assert "/summarize" in data["paths"]

    assert "/learn/recommendations" in data["paths"]