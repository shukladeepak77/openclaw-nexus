from fastapi.testclient import TestClient
from app import app


def test_analyze_upload_basic():
    client = TestClient(app)
    content = (
        "INFO: User login\n"
        "ERROR: invalid password\n"
        "INFO: User login\n"
        "INFO: User logout\n"
        "ERROR: invalid password\n"
    )
    files = {"file": ("log.txt", content, "text/plain")}
    response = client.post("/analyze", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "counts" in data
    assert "top_messages" in data
    assert data["counts"]["INFO: User login"] == 2
    assert data["counts"]["ERROR: invalid password"] == 2
    # Top messages should include the two most frequent lines
    top = data["top_messages"]
    assert isinstance(top, list)
    assert "INFO: User login" in top
    assert "ERROR: invalid password" in top
    assert len(top) <= 3
