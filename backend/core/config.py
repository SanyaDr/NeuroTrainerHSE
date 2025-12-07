from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings():
    # ====== ОБЪЯВЛЯЕМ ВСЕ ПОЛЯ ТУТ ======
    app_name: str = "NeuroCoach Vibe"
    openrouter_api_key: str  # берётся из .env

    # если есть ещё что-то (DB_URL, DEBUG и т.п.), добавь сюда:
    database_url: str = "sqlite:///./neurocoach.db"
    debug: bool = True
    api_prefix: str = "/api"


    # ====== КОНФИГ Pydantic v2 ======
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# НИКАКОГО своего __init__ тут не нужно!
settings = Settings()