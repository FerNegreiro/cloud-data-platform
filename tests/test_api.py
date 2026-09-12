from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "online",
        "service": "Cloud Data Platform API"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "api": "online",
        "database": "connected"
    }