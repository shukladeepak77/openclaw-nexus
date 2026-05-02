from fastapi.testclient import TestClient
from app import app


def test_incident_high_error():
    client = TestClient(app)
    logs = "\n".join(["ERROR: something failed"] * 6 + ["DB connection failed"])
    payload = {
        "service": "auth-service",
        "environment": "prod",
        "logs": logs,
    }
    response = client.post("/incident/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "HIGH"
    assert isinstance(data["suggested_actions"], list)
    assert "Database" in data["root_cause"] or "DB" in data["root_cause"]


def test_incident_medium_timeout_pattern():
    client = TestClient(app)
    logs = "timeout during request\nWARNING slow response"
    payload = {
        "service": "web-service",
        "environment": "staging",
        "logs": logs,
    }
    response = client.post("/incident/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] in ("MEDIUM", "HIGH")
    assert isinstance(data["suggested_actions"], list)

