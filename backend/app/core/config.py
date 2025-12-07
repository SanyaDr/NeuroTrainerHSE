import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Основные настройки
    app_name: str = "NeuroCoach Vibe"
    debug: bool = True
    api_prefix: str = "/api/v1"

    # API ключи
    openrouter_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # База данных
    database_url: str = "sqlite:///./neurocoach.db"

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


# Создаем экземпляр настроек
settings = Settings()

# Перезаписываем из переменных окружения, если они есть
settings.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", settings.openrouter_api_key)
settings.openai_api_key = os.getenv("OPENAI_API_KEY", settings.openai_api_key)
settings.database_url = os.getenv("DATABASE_URL", settings.database_url)