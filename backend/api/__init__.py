"""
API модуль - содержит все эндпоинты
"""

from .endpoints import vibe, workout, coach, profile, forecast

__all__ = [
    "vibe",
    "workout",
    "coach",
    "profile",
    "forecast",
]