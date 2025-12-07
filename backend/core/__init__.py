"""
Ядро приложения
"""

from backend.core.config import settings
from backend.core.database import (
    Base,
    engine,
    SessionLocal,
    get_db,
    create_tables
)

__all__ = [
    "settings",
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "create_tables"
]