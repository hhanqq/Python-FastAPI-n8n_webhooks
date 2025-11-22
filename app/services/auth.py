from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserLogin
from app.utils.security import verify_password
from app.utils.default_values import DEFAULT_ROLE


async def authenticate_user(user_data: UserLogin, db: AsyncSession) -> User | None:
    query = select(User).where(User.username == user_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()


    if not user or not verify_password(user_data.password, user.hashed_password):
        return None

    if user.role == DEFAULT_ROLE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ваша заявка в обработке. Доступ ограничен."
        )

    return user
