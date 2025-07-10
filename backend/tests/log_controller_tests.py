import pytest
import json
from datetime import date
from backend.__main__ import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_logs(client):
    response = client.get("/api/logs")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_logs_by_valid_id(client):
    response = client.get("/api/logs")
    logs = response.get_json()

    if not logs:
        pytest.skip("No logs available to test by ID.")

    log_id = logs[0]["id"]
    response = client.get(f"/api/logs/{log_id}")
    assert response.status_code == 200
    assert response.get_json()["id"] == log_id


def test_log_lifecycle(client):
    # CREATE
    payload = {
        "title": "Lifecycle Test",
        "entries": "Testing create -> update -> delete",
        "log_date": date.today().isoformat(),
        "tags": ["lifecycle"],
        "mood": "curious"
    }

    response = client.post("/api/logs", json=payload)
    assert response.status_code == 201
    log_id = response.headers.get("message", "").split(" ")[1]
    assert log_id

    # UPDATE
    updated_payload = {
        "title": "Updated Title",
        "entries": "Now updated",
        "log_date": date.today().isoformat(),
        "tags": ["updated"],
        "mood": "reflective"
    }

    response = client.put(f"/api/logs/{log_id}", json=updated_payload)
    assert response.status_code == 204

    # DELETE
    response = client.delete(f"/api/logs/{log_id}")
    assert response.status_code == 204

    # Confirm deletion
    response = client.get(f"/api/logs/{log_id}")
    assert response.status_code == 404






