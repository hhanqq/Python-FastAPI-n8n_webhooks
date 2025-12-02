from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.email import EmailCreate, EmailResponse, EmailUpdateStatus
from app.models.email import EmailStatus
from app.crud.email import create_email, get_emails_on_approval, get_email_by_id, update_email_status, remove_email
from app.services.n8n_wh_emails import send_email_to_n8n
from app.utils.dependencies import get_current_user
from app.schemas.user import UserPublic
from app.crud.email import get_all_emails


router = APIRouter(prefix="/emails", tags=["Emails"])


@router.post(
    "/webhook",
    status_code=status.HTTP_201_CREATED,
    response_model=EmailResponse,
    summary="Принять новое письмо (Webhook)",
    description="""
    Эндпоинт для приема данных от n8n или других внешних систем.

    - Создает запись в БД со статусом on_approval.
    - Не требует авторизации пользователя (публичный API для роботов).
    """,
    responses={
        201: {
            "description": "Письмо успешно сохранено",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "text_content": "Привет, мир!",
                        "html_content": "<p>Привет, мир!</p>",
                        "status": "on_approval",
                        "created_at": "2023-10-25T12:00:00"
                    }
                }
            }
        }
    }
)
async def receive_email_webhook(
        email_data: EmailCreate = Body(..., description="Данные письма (текст или HTML)"),
        db: Annotated[AsyncSession, Depends(get_db)] = None
):
    return await create_email(db=db, email_in=email_data)


@router.get(
    "/pending",
    response_model=List[EmailResponse],
    summary="Получить список писем на модерации",
    description="Возвращает список всех писем, у которых статус on_approval. Требует токен авторизации.",
    responses={
        200: {"description": "Список писем получен"},
        401: {"description": "Пользователь не авторизован"}
    }
)
async def get_pending_emails(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[UserPublic, Depends(get_current_user)],
        skip: int = 0,
        limit: int = 1000,
):
    return await get_emails_on_approval(db, skip=skip, limit=limit)


@router.patch(
    "/{email_id}/status",
    response_model=EmailResponse,
    summary="Изменить статус письма (Одобрить/Отклонить)",
    description="""
    Меняет статус указанного письма.

    Логика работы:
    - Если статус изменен на approved -> запускается фоновая задача отправки вебхука обратно в n8n.
    - Если статус rejected или edited -> просто обновляется запись в БД.
    """,
    responses={
        200: {"description": "Статус успешно обновлен"},
        404: {"description": "Письмо с таким ID не найдено"},
        401: {"description": "Необходима авторизация"}
    }
)
async def update_status(
        background_tasks: BackgroundTasks,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[UserPublic, Depends(get_current_user)],
        email_id: int = Path(..., description="ID письма в базе данных", ge=1),
        status_data: EmailUpdateStatus = Body(..., description="Новый статус для установки"),
):
    email = await get_email_by_id(db, email_id)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )

    updated_email = await update_email_status(db, email, status_data.status)

    if updated_email.status == EmailStatus.APPROVED:
        email_schema = EmailResponse.model_validate(updated_email)
        background_tasks.add_task(send_email_to_n8n, email_schema)

    return updated_email


@router.get(
    "/all",
    response_model=List[EmailResponse],
    summary="Получить все письма (Архив)",
    description="""
    Возвращает список всех писем, хранящихся в базе данных, с любыми статусами.

    Требует авторизации пользователя.
    """,
    responses={
        200: {"description": "Список всех писем получен"},
        401: {"description": "Пользователь не авторизован"}
    }
)
async def get_emails_all(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[UserPublic, Depends(get_current_user)],
):
    return await get_all_emails(db)


@router.delete(
    "/{email_id}/delete",
    response_model=EmailResponse,
)
async def delete_email(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[UserPublic, Depends(get_current_user)],
        email_id: int = Path(..., description="ID письма в базе данных", ge=1),
):
    return await remove_email(db, email_id)