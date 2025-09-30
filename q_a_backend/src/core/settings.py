from functools import lru_cache
import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    # CORS: allow Angular dev ports and wildcard as fallback
    cors_allow_origins: list[str] = Field(
        default_factory=lambda: os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
        if os.getenv("CORS_ALLOW_ORIGINS")
        else ["*"]
    )
    # Placeholder for future DB URL integration
    database_url: str | None = Field(default=os.getenv("DATABASE_URL"))


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()


# Expose a module-level settings for convenience
settings = get_settings()
