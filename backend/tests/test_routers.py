import pytest
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_welcome():
    response = client.get("/welcome")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the AI Agent"
    }
