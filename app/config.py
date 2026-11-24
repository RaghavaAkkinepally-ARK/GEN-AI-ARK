from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AgricultureGPT"
    environment: str = "development"
    secret_key: str = "development-only-change-me"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "agriculture_gpt"
    chroma_persist_directory: str = "./data/chroma"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    default_llm_provider: str = "mock"
    default_llm_model: str = "agriculture-gpt-demo"
    openai_api_key: str | None = None
    hf_token: str | None = None
    weather_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()

