from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорты из нашего пакета
from backend.core.config import settings
from backend.core.database import create_tables
from backend.api.endpoints import (
    vibe_router,
    workout_router,
    coach_router,
    profile_router,
    forecast_router,
)
# Создаем таблицы при старте
create_tables()

app = FastAPI(
    title=settings.app_name,
    description="AI-тренер для персонализированных тренировок",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    debug=settings.debug,
)


@app.get("/api/ping")
async def ping():
    return {"status": "ok"}
    
# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Временное упрощение
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем только работающие роутеры
app.include_router(vibe_router, prefix=settings.api_prefix, tags=["vibe"])
# Остальные закомментированы до создания
app.include_router(workout_router, prefix=settings.api_prefix, tags=["workout"])
app.include_router(coach_router, prefix=settings.api_prefix, tags=["coach"])
app.include_router(profile_router, prefix=settings.api_prefix, tags=["profile"])
app.include_router(forecast_router, prefix=settings.api_prefix, tags=["forecast"])


@app.get("/")
async def root():
    return {
        "message": settings.app_name,
        "status": "running",
        "version": "1.0.0",
        "debug": settings.debug,
        "docs": "/api/docs",
        "available_endpoints": [
            f"{settings.api_prefix}/vibe"
        ],
        "endpoints_coming_soon": [
            f"{settings.api_prefix}/workout",
            f"{settings.api_prefix}/coach",
            f"{settings.api_prefix}/profile",
            f"{settings.api_prefix}/forecast"
        ]
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "active_routers": 1,
        "database": "SQLite"
    }


@app.get("/api/test")
async def test_api():
    """Тестовый эндпоинт для проверки работы"""
    return {
        "success": True,
        "message": "API работает!",
        "active_endpoint": f"{settings.api_prefix}/vibe",
        "test_request": {
            "method": "POST",
            "url": f"{settings.api_prefix}/vibe/assess",
            "body": {
                "user_input": "Устал после работы, но хочу потрениться",
                "fatigue_level": 4,
                "stress_level": 3,
                "motivation_level": 2
            }
        }
    }


@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения"""
    print(f"🚀 {settings.app_name} запущен!")
    print(f"🔧 Режим отладки: {settings.debug}")
    print(f"📚 Документация: http://localhost:8000/api/docs")
    print(f"🎯 Активный эндпоинт: POST {settings.api_prefix}/vibe/assess")


@app.on_event("shutdown")
async def shutdown_event():
    """Действия при остановке приложения"""
    print(f"👋 {settings.app_name} остановлен")