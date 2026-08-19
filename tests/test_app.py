from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_status():
    response = client.get("/api/status")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_successful_request():
    response = client.post("/api/request")

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_simulated_error():
    response = client.post("/api/error")

    assert response.status_code == 500


def test_slow_request():
    response = client.post("/api/slow")

    assert response.status_code == 200