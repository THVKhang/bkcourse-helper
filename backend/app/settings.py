from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator
from typing import List
import warnings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), env_file_encoding="utf-8", extra="ignore")

    DB_URL: str = "sqlite:///./bkcourse.db"
    CORS_ORIGINS: str = "http://localhost:3000"
    DEBUG: bool = False
    JWT_SECRET: str = ""
    SUPABASE_JWT_SECRET: str = ""  # legacy name, still honoured
    RESEND_API_KEY: str = ""

    @field_validator("CORS_ORIGINS")
    @classmethod
    def normalize_cors(cls, v: str) -> str:
        # allow comma-separated
        return v

    def cors_list(self) -> List[str]:
        return [s.strip() for s in self.CORS_ORIGINS.split(",") if s.strip()]


    def jwt_secret(self) -> str:
        secret = self.JWT_SECRET or self.SUPABASE_JWT_SECRET
        if secret:
            return secret
        warnings.warn(
            "JWT_SECRET is not set; using an insecure development key. "
            "Set JWT_SECRET in production!",
            stacklevel=2,
        )
        return "bkcourse-helper-insecure-dev-key-change-me-in-production"


settings = Settings()
