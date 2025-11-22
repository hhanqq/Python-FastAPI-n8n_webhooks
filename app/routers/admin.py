from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.database import get_db
from app.services.admin import manage_role
from app.utils.dependencies import get_current_admin_user


router = APIRouter(prefix='/admin', tags=['Admin'])


@router.patch(
    "/{user_id}/role",
    response_model=dict,
    summary="Изменить права доступа пользователя",
    description="Обновляет роль пользователя (дает доступ к системе). Доступно только **администраторам**.",
    responses={
        200: {"description": "Роль успешно обновлена"},
        403: {"description": "Недостаточно прав"},
        404: {"description": "Пользователь не найден"}
    }
)
async def change_user_role(
    user_id: int = Path(..., description="ID пользователя", ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    updated_user = await manage_role(user_id, db)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return {"message": f"Пользователь {user_id} допущен к системе"}