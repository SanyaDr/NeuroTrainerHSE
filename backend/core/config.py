from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Название приложения
    app_name: str = "NeuroCoach Vibe"

    # Префикс для всех API маршрутов
    api_prefix: str = "/api"

    # 🔑 Ключ для OpenRouter — ОБЯЗАТЕЛЬНОЕ поле
    openrouter_api_key: str

    debug: bool = True


    # URL базы данных
    database_url: str = "sqlite:///./neurocoach.db"

    # Настройки pydantic-settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# Глобальный объект настроек
settings = Settings()

print("DEBUG KEY:", bool(settings.openrouter_api_key))
