"""Application configuration settings for Thirai Kuzhu AI.

Follows PEP 257 Google-style docstrings and Pydantic v2 BaseSettings.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for GCP, Grafana Cloud MCP, and Agent meshes."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    APP_NAME: str = Field(default="Thirai Kuzhu AI", description="Application Title")
    ENV: str = Field(default="development", description="Runtime environment")
    PORT: int = Field(default=8080, description="Server port")
    LOG_LEVEL: str = Field(default="INFO", description="Structured logging level")

    # Google Cloud
    GOOGLE_CLOUD_PROJECT: str = Field(
        default="genai-blockbuster-2026", description="GCP Project ID"
    )
    GOOGLE_CLOUD_LOCATION: str = Field(
        default="us-central1", description="Default Vertex AI region"
    )
    GEMINI_API_KEY: str = Field(
        default="", description="Optional API key fallback for local ADK testing"
    )

    # Core Gemini Model Tiers
    PRIMARY_MODEL: str = Field(
        default="gemini-3.8-flash-001", description="High-throughput telemetry triage model"
    )
    DIRECTOR_MODEL: str = Field(
        default="gemini-3.8-pro-001", description="Deep reasoning director orchestration model"
    )

    # Grafana Cloud MCP Partner Track
    GRAFANA_URL: str = Field(
        default="https://thiraikuzhu.grafana.net",
        description="Base URL for your Grafana Cloud stack",
    )
    GRAFANA_MCP_ENDPOINT: str = Field(
        default="https://mcp.grafana.com/mcp",
        description="Hosted Grafana Cloud MCP streamable HTTP endpoint",
    )
    GRAFANA_TOKEN: str = Field(default="", description="Grafana Service Account Token (glsa_...)")

    # Execution Quotas & Guardrails
    MAX_MISSION_DURATION_SECONDS: int = Field(
        default=60, description="Circuit breaker max execution time per investigation"
    )
    MAX_TOOL_CALLS_PER_MISSION: int = Field(
        default=8, description="Max MCP tool queries allowed per incident"
    )
    MAX_TOKEN_BUDGET: int = Field(
        default=16000, description="Token limit per mission to prevent runaway loops"
    )

    # Security & Authentication
    AUTH_ENABLED: bool = Field(
        default=False, description="Enable Firebase / Google Cloud Identity token authentication"
    )


@lru_cache
def get_settings() -> Settings:
    """Returns cached application settings singleton.

    Returns:
        Settings: Validated configuration instance.
    """
    return Settings()
