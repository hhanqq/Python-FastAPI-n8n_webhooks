import httpx
import logging
from app.schemas.email import EmailResponse
from app.core.config import settings

logger = logging.getLogger("uvicorn.error")


async def send_email_to_n8n(email: EmailResponse):
    url = settings.N8N_WEBHOOK_URL

    logger.info(f"🔄 [Background] Начинаю отправку вебхука для email id={email.id} на {url}...")

    if not url:
        logger.warning("⚠️ [Background] N8N_WEBHOOK_URL не задан, пропускаю.")
        return

    async with httpx.AsyncClient() as client:
        payload = {
            "id": email.id,
            "text_content": email.text_content,
            "html_content": email.html_content,
            "status": email.status.value,
            "created_at": email.created_at.isoformat() if email.created_at else None
        }
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()

            logger.info(f"✅ [Background] Вебхук успешно отправлен! Ответ сервера: {response.status_code}")

        except Exception as e:
            logger.error(f"❌ [Background] Ошибка отправки в n8n: {e}")