from pydantic import BaseSettings, Field, validator
from typing import Optional

class Settings(BaseSettings):
    # Core
    SERVICE_NAME: str = "unknown"
    ENV: str = "dev"

    # Networking
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # LLM Keys
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None

    # Orchestrator routing
    ORCHESTRATOR_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("PORT")
    def validate_port(cls, v):
        if v <= 0:
            raise ValueError("PORT must be > 0")
        return v

settings = Settings()