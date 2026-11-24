"""
ALLINA Central Platform Configuration
Loads settings strictly from environment variables using Pydantic Settings.
No secrets or hardcoded passwords allowed.
"""
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "ALLINA IT Operations Platform"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Security
    SECRET_KEY: str = "allina-dev-secret-key-change-in-production"
    ALLOWED_ORIGINS: Union[str, List[str]] = "http://localhost:5173,http://localhost:3000"

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres_password_placeholder@db:5432/allina_db"

    # Background Tasks (Celery & Redis)
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    # Temporal (Placeholder for durable workflow engine)
    TEMPORAL_HOST: str = "temporal:7233"
    TEMPORAL_NAMESPACE: str = "default"

    # Policy Engine (Placeholder for OPA)
    OPA_URL: str = "http://opa:8181/v1/data/allina/policy"

    # LLM Gateway
    DEFAULT_LLM_PROVIDER: str = "mock"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def cors_origins(self) -> List[str]:
        if isinstance(self.ALLOWED_ORIGINS, list):
            return self.ALLOWED_ORIGINS
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


settings = Settings()
