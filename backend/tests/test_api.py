from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_and_get_research():
    payload = {
        "question": "Analyze AI adoption in Canada",
        "depth": "standard",
    }

    response = client.post(
        "/api/v1/research",
        json=payload,
    )

    assert response.status_code == 201

    job = response.json()

    assert job["status"] == "queued"
    assert job["question"] == payload["question"]

    research_id = job["research_id"]

    get_response = client.get(
        f"/api/v1/research/{research_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["research_id"] == research_id


def test_invalid_question():
    response = client.post(
        "/api/v1/research",
        json={"question": "Hi"},
    )

    assert response.status_code == 422


def test_missing_research_job():
    response = client.get(
        "/api/v1/research/"
        "550e8400-e29b-41d4-a716-446655440000"
    )

    assert response.status_code == 404
