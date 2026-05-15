from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    BOT_TOKEN: str
    CHANNEL_ID: str
    ADMIN_IDS: list[int] = Field(default_factory=list)

    OPENAI_API_KEY: str
    OPENAI_MODEL_MAIN: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.65
    MAX_TOKENS: int = 2000

    TAVILY_API_KEY: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379/0"

    AUTO_PUBLISH: bool = False
    DRY_RUN: bool = True

settings = Settings()