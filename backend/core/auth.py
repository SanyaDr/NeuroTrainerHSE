from datetime import datetime, timedelta
from typing import Optional

import hashlib
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

# =========================
# НАСТРОЙКИ JWT И БЕЗОПАСНОСТИ
# =========================

# ⚠️ В проде вынести в env / конфиг
SECRET_KEY = "change-this-secret-key-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # сколько живёт access-токен

# Схема авторизации через заголовок Authorization: Bearer <token>
security = HTTPBearer()


# =========================
# РАБОТА С ПАРОЛЯМИ
# =========================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Сравнение обычного пароля с захешированным.
    Сейчас используется SHA256 как временное решение.
    """
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def get_password_hash(password: str) -> str:
    """
    Хэширование пароля.
    TODO: заменить на passlib/bcrypt в проде.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# =========================
# JWT-ТОКЕНЫ
# =========================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создаёт JWT-токен.
    В data обычно передаём {"sub": email} или {"sub": user_id}.
    """
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# =========================
# АУТЕНТИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ
# =========================

def authenticate_user(db: Session, email: str, password: str):
    """
    Проверка логина/пароля.
    Возвращает объект пользователя или False.
    """
    user = crud.get_user_by_email(db, email)
    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


# =========================
# ЗАВИСИМОСТИ ДЛЯ FASTAPI
# =========================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Получить текущего пользователя из Bearer-токена.

    - Берём токен из заголовка Authorization.
    - Декодим JWT.
    - Достаём email из payload["sub"].
    - Находим юзера в БД.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        # Нет токена вообще
        raise credentials_exception

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
):
    """
    Проверяем, что пользователь активен.
    Можно использовать как Depends в защищённых эндпоинтах.
    """
    if not getattr(current_user, "is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# =========================
# ЭКСПОРТ ДЛЯ ДРУГИХ МОДУЛЕЙ
# =========================

__all__ = [
    "SECRET_KEY",
    "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "authenticate_user",
    "get_current_user",
    "get_current_active_user",
]
