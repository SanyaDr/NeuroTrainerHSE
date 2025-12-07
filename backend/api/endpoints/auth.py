from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional

from ...core.database import get_db
from ...core.auth import (
    authenticate_user,
    create_tokens,
    get_current_user,
    get_current_active_user,
    get_current_premium_user,
    verify_refresh_token,
    get_password_hash
)
from .schemas.auth import (
    UserCreate,
    UserResponse,
    UserUpdate,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    AuthResponse
)
from backend.models.user import User

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register(
        user_data: UserCreate,
        db: Session = Depends(get_db),
        background_tasks: BackgroundTasks = None
):
    """Регистрация нового пользователя"""
    # Проверяем существование пользователя
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем уже существует"
            )

    # Создаем пользователя
    hashed_password = get_password_hash(user_data.password)

    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_active=True,
        is_verified=False,
        is_premium=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Создаем токены
    tokens = create_tokens(user)

    # Здесь можно добавить отправку email подтверждения
    # if background_tasks:
    #     background_tasks.add_task(send_verification_email, user.email)

    return AuthResponse(
        success=True,
        message="Регистрация прошла успешно",
        data={
            "tokens": tokens.dict(),
            "user": user.to_dict()
        }
    )


@router.post("/login", response_model=AuthResponse)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """Вход пользователя"""
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens = create_tokens(user)

    return AuthResponse(
        success=True,
        message="Вход выполнен успешно",
        data={
            "tokens": tokens.dict(),
            "user": user.to_dict()
        }
    )


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
        token_data: RefreshTokenRequest,
        db: Session = Depends(get_db)
):
    """Обновление access токена с помощью refresh токена"""
    user = await verify_refresh_token(token_data.refresh_token, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh токен"
        )

    tokens = create_tokens(user)

    return AuthResponse(
        success=True,
        message="Токен обновлен",
        data={
            "tokens": tokens.dict(),
            "user": user.to_dict()
        }
    )


@router.get("/me", response_model=AuthResponse)
async def get_current_user_info(
        current_user: User = Depends(get_current_active_user)
):
    """Получение информации о текущем пользователе"""
    return AuthResponse(
        success=True,
        message="Информация о пользователе",
        data={"user": current_user.to_dict()}
    )


@router.put("/me", response_model=AuthResponse)
async def update_current_user(
        user_data: UserUpdate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Обновление информации о пользователе"""
    update_data = user_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return AuthResponse(
        success=True,
        message="Данные обновлены",
        data={"user": current_user.to_dict()}
    )


@router.post("/logout", response_model=AuthResponse)
async def logout(
        current_user: User = Depends(get_current_active_user)
):
    """Выход пользователя (на клиенте нужно удалить токены)"""
    return AuthResponse(
        success=True,
        message="Вы успешно вышли из системы"
    )


@router.post("/password/reset", response_model=AuthResponse)
async def request_password_reset(
        reset_data: PasswordResetRequest,
        db: Session = Depends(get_db),
        background_tasks: BackgroundTasks = None
):
    """Запрос на сброс пароля"""
    user = db.query(User).filter(User.email == reset_data.email).first()

    if user and user.is_active:
        # Генерируем токен сброса пароля
        reset_token = create_tokens(user).access_token  # Используем access токен как пример

        # Здесь можно добавить отправку email с токеном
        # if background_tasks:
        #     background_tasks.add_task(send_password_reset_email, user.email, reset_token)

        return AuthResponse(
            success=True,
            message="Инструкции по сбросу пароля отправлены на email",
            data={"reset_token": reset_token}  # В продакшене не возвращаем токен!
        )

    # Всегда возвращаем успех, даже если пользователя нет (security through obscurity)
    return AuthResponse(
        success=True,
        message="Если пользователь существует, инструкции будут отправлены на email"
    )


@router.post("/password/reset/confirm", response_model=AuthResponse)
async def confirm_password_reset(
        reset_data: PasswordResetConfirm,
        db: Session = Depends(get_db)
):
    """Подтверждение сброса пароля"""
    # Валидация токена
    from backend.core.security import get_token_payload
    payload = get_token_payload(reset_data.token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недействительный токен"
        )

    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат токена"
        )

    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    # Обновляем пароль
    user.hashed_password = get_password_hash(reset_data.new_password)
    db.commit()

    return AuthResponse(
        success=True,
        message="Пароль успешно изменен"
    )


@router.get("/premium/check", response_model=AuthResponse)
async def check_premium_status(
        current_user: User = Depends(get_current_active_user)
):
    """Проверка премиум статуса"""
    return AuthResponse(
        success=True,
        message="Статус премиум",
        data={"is_premium": current_user.is_premium}
    )


# Административные эндпоинты (только для теста/админа)
@router.get("/users", response_model=AuthResponse)
async def get_all_users(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Получение всех пользователей (только для админа)"""
    # Простая проверка на админа (в реальном проекте нужна полноценная система ролей)
    if current_user.email != "admin@example.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )

    users = db.query(User).all()
    return AuthResponse(
        success=True,
        message="Список пользователей",
        data={"users": [user.to_dict() for user in users]}
    )