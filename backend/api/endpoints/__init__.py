"""
Эндпоинты API
"""

from vibe import router as vibe_router
from workout import router as workout_router
from coach import router as coach_router
from profile import router as profile_router
from forecast import router as forecast_router

__all__ = [
    "vibe_router",
    "workout_router",
    "coach_router",
    "profile_router",
    "forecast_router",
]