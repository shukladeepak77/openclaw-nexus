from fastapi.testclient import TestClient
from app import app


def test_chatops_page():
    client = TestClient(app)
    resp = client.get("/chatops")
    assert resp.status_code == 200
    assert "ChatOps Console" in resp.text or resp.text.strip().startswith("<")


def test_chatops_message_check_disk():
    client = TestClient(app)
    response = client.post("/chatops/message", json={"message": "check disk"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "Disk usage" in data["response"]


def test_nl_memory_ok():
    client = TestClient(app)
    response = client.post("/chatops/message", json={"message": "is memory ok?"})
    assert response.status_code == 200
    data = response.json()
    assert "Memory usage" in data.get("response", "")


def test_nl_ports_open():
    client = TestClient(app)
    response = client.post("/chatops/message", json={"message": "are ports open?"})
    assert response.status_code == 200
    data = response.json()
    assert "Open ports" in data.get("response", "")
