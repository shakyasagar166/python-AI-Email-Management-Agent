"""
Application Configuration Settings
"""
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
DB_FILE = BACKEND_DIR / "email_agent.db"
SCHEMA_FILE = PROJECT_ROOT / "database" / "schema.sql"
SAMPLE_DATA_FILE = PROJECT_ROOT / "database" / "sample_data.sql"


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "MailMind AI Email Agent")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # Database
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", str(DB_FILE))
    SCHEMA_PATH: str = str(SCHEMA_FILE)
    SAMPLE_DATA_PATH: str = str(SAMPLE_DATA_FILE)

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-mailmind-jwt-key-2026")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

    # AI / LLM
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock").lower()
    DEFAULT_LLM_PROVIDER: str = LLM_PROVIDER
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_AI_MODEL", "gpt-4o-mini")
    DEFAULT_LLM_MODEL: str = DEFAULT_MODEL
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.3))


settings = Settings()
