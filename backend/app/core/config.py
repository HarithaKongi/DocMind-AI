from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DocMind AI API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:3000"]

    supabase_url: str = ""
    supabase_key: str = ""

    embedding_api_key: str = ""
    embedding_api_url: str = "https://api.openai.com/v1/embeddings"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    llm_api_key: str = ""
    llm_api_url: str = "https://api.openai.com/v1/chat/completions"
    llm_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
