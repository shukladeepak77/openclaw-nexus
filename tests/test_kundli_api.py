from fastapi.testclient import TestClient
from app import app


def test_kundli_analyze_basic():
    client = TestClient(app)
    payload = {
        "dob": "1990-01-01",
        "time": "12:00",
        "place": "New York",
        "gender": "Male",
    }
    response = client.post("/kundli/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Expect the four placeholder insights
    assert "personality" in data
    assert "career" in data
    assert "challenges" in data
    assert "guidance" in data


def test_kundli_analyze_afternoon_specific():
    client = TestClient(app)
    payload = {
        "dob": "1977-04-12",
        "time": "14:03",
        "place": "Delhi",
        "gender": None,
    }
    response = client.post("/kundli/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["personality"] == "Afternoon profile: practical, grounded, work-focused."
    assert data["career"] == "Afternoon career path: practical tasks and steady execution."
    assert data["challenges"] == "Afternoon challenges: avoid creative block and fatigue."
    assert data["guidance"] == "Afternoon guidance: chunk work into clear milestones."
