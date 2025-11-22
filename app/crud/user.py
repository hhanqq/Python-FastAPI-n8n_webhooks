from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash
from app.utils.default_values import DEFAULT_ROLE



async def create_user(user_data: UserCreate, db: AsyncSession) -> User | None:
    query = select(User).where(User.username == user_data.username)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        return None

    hashed_password = get_password_hash(user_data.password)

    db_user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        role=DEFAULT_ROLE,
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user