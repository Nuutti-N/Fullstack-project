import os
import pytest
from fastapi.testclient import TestClient


# @pytest.fixture(scope="session", autouse=True)
# def set_deest_env():
# os.environ.setdefault(
#     "database_url", "postgresql://postgres.wusdjwchnnixubviapya:[YOUR-PASSWORD]@aws-1-eu-west-1.pooler.supabase.com:6543/postgres")
# os.environ.setdefault("jwt_key", "test_jwt_key")
# os.environ.setdefault("jwt_refresh_key", "test_jwt_refresh_key")
# os.environ.setdefault("algorithm", "HS256")
# os.environ.setdefault("supabase_url", "http://localhost:54321")
# os.environ.setdefault("supabase_key", "test_supabase_key")
# os.environ.setdefault("gemini_api_key", "test_gemini_api_key")


@pytest.fixture(scope="session", autouse=True)
def client():
    from backend.main import app
    return TestClient(app)
