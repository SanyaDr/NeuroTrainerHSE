"""
Эндпоинты API
"""

from backend.api.endpoints.vibe import router as vibe_router
from backend.api.endpoints.workout import router as workout_router
from backend.api.endpoints.coach import router as coach_router
from backend.api.endpoints.profile import router as profile_router
from backend.api.endpoints.forecast import router as forecast_router

__all__ = [
    "vibe_router",
    "workout_router",
    "coach_router",
    "profile_router",
    "forecast_router",
]