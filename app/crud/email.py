from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.email import Email, EmailStatus
from app.schemas.email import EmailCreate

async def create_email(db: AsyncSession, email_in: EmailCreate) -> Email:
    db_email = Email(
        text_content=email_in.text_content,
        html_content=email_in.html_content,
        status=EmailStatus.ON_APPROVAL
    )
    db.add(db_email)
    await db.commit()
    await db.refresh(db_email)
    return db_email

async def get_emails_on_approval(db: AsyncSession, skip: int = 0, limit: int = 100):
    # В AsyncAlchemy запросы строятся чуть иначе (через select)
    query = select(Email).filter(Email.status == EmailStatus.ON_APPROVAL).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_email_by_id(db: AsyncSession, email_id: int):
    query = select(Email).filter(Email.id == email_id)
    result = await db.execute(query)
    return result.scalars().first()

async def update_email_status(db: AsyncSession, email: Email, status: str):
    email.status = status
    db.add(email) # Помечаем объект как измененный
    await db.commit()
    await db.refresh(email)
    return email


async def get_all_emails(db: AsyncSession):
    query = select(Email).order_by(Email.id)
    result = await db.execute(query)
    return result.scalars().all()


async def remove_email(db: AsyncSession, email_id: int):
    result = await db.execute(
        select(Email).where(Email.id == email_id)
    )
    email = result.scalar_one_or_none()

    if not email:
        return None

    await db.delete(email)
    await db.commit()
    return email


async def edit_email(db: AsyncSession, email: Email, email_id: int):
    result = await db.execute(
        select(Email).where(Email.id == email_id)
    )
    email = result.scalar_one_or_none()

    if not email:
        return None

