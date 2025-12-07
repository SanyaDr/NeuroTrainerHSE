"""
API модуль - содержит все эндпоинты
"""

from fastapi import APIRouter
from backend.api.endpoints import coach_router, vibe_router, workout_router, profile_router, forecast_router

api_router = APIRouter()
api_router.include_router(coach_router, prefix="/coach", tags=["coach"])
# остальное по желанию
