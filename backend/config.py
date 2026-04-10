import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):

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

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

# If All found, start it, if any missing, show error


settings = Settings()
