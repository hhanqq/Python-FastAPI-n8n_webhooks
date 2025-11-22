from app.models.user import User
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def manage_role(user_id: int, db: AsyncSession) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        return None

    user.role = "approved"


    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user