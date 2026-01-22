from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_name: str = "SAFE Governance Agent"
    environment: str = "development"
    log_level: str = "INFO"

    # Admin / Security
    admin_api_key: str | None = None

    # AI Providers
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    together_api_key: str | None = None

    # Models
    openai_model: str = "gpt-4o"
    anthropic_model: str = "claude-3-sonnet"
    fallback_model: str = "mistral-7b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
