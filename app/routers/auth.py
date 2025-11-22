from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserPublic
from app.services.auth import authenticate_user
from app.crud.user import create_user
from app.utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
    summary="Регистрация нового пользователя",
    description="Создает нового пользователя в системе. **Username** должен быть уникальным.",
    responses={
        201: {"description": "Пользователь успешно создан"},
        400: {"description": "Пользователь с таким именем уже существует"}
    }
)
async def register(
        user_data: UserCreate,
        db: Annotated[AsyncSession, Depends(get_db)]
):

    user = await create_user(user_data=user_data, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return user


@router.post(
    "/login",
    summary="Вход в систему",
    description="Проверяет логин/пароль и устанавливает безопасную **HttpOnly cookie** с токеном доступа.",
    responses={
        200: {"description": "Успешный вход"},
        401: {"description": "Неверное имя пользователя или пароль"}
    }
)
async def login(
        response: Response,
        user_data: UserLogin,
        db: Annotated[AsyncSession, Depends(get_db)]
):

    user = await authenticate_user(user_data=user_data, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": user.username})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True,
        path="/",
        max_age=10800,
    )

    return {"message": "Logged in successfully"}


@router.post(
    "/logout",
    summary="Выход из системы",
    description="Завершает сессию пользователя, удаляя cookie **access_token**.",
    responses={
        200: {"description": "Успешный выход"}
    }
)
async def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Logged out successfully"}