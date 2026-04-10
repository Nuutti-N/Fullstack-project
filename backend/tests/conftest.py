from fastapi.testclient import TestClient
import pytest


@pytest.fixture()
def client():
    from backend.main import app
    return TestClient(app)
