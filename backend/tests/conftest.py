from backend import models
from backend.database import engine
from sqlmodel import SQLModel
import os
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def set_deest_env():
    os.environ["database_url"] = "postgresql+psycopg2://postgres:postgres@localhost:5433/test_db"
    os.environ["jwt_key"] = "test_jwt_key"
    os.environ["jwt_refresh_key"] = "test_jwt_refresh_key"
    os.environ["algorithm"] = "HS256"
    os.environ["supabase_url"] = "http://localhost:54321"
    os.environ["supabase_key"] = "test_supabase_key"
    os.environ["gemini_api_key"] = "test_gemini_api_key"


SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)


@pytest.fixture()
def client():
    from backend.main import app
    return TestClient(app)
