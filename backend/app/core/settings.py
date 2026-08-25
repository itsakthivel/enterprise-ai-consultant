from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

environment = os.getenv("APP_ENV", "dev")


class Settings(BaseSettings):

    app_name: str = "Enterprise AI Consultant"
    app_version: str = "0.1.0"
    app_env: str = "dev"

    api_host: str = "127.0.0.1"
    api_port: int = 8000

    database_url: str
    vector_db_collection: str

    rag_chunk_size: int = Field(default=1000, gt=0)
    rag_chunk_overlap: int = Field(default=200, ge=0)
    embedding_model: str = "all-MiniLM-L6-v2"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=f".env.{environment}",
        extra="ignore"
    )


settings = Settings()
