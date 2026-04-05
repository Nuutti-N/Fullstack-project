from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict
# When my app starts: look in .env


class Setting(BaseSettings):
    # Database
    database_url: str

    # User
    jwt_key: str
    jwt_refresh_key: str
    algorithm: str = "HS256"

    # Supabase
    supabase_url: str
    supabase_key: str

    # LLM
    gemini_api_key: str


settings = Setting()
# If All found, start it, if any missing, show error
