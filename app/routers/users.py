from typing import Annotated
from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserPublic

router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    "/me",
    response_model=UserPublic,
    summary="Получить текущего пользователя",
    description="Возвращает публичные данные текущего авторизованного пользователя. Требует валидный **access_token** в cookies.",
    responses={
        200: {"description": "Данные пользователя получены"},
        401: {"description": "Пользователь не авторизован"}
    }
)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user