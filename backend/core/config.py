import os
from typing import Optional


class Settings:
    """Настройки приложения"""

    def __init__(self):
        # Основные настройки
        self.app_name: str = "NeuroCoach Vibe"
        self.debug: bool = True
        self.api_prefix: str = "/api/v1"

        # API ключи
        self.openrouter_api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")

        # База данных
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "sqlite:///./neurocoach.db"
        )

        # CORS
        self.cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]


# Создаем экземпляр настроек
settings = Settings()