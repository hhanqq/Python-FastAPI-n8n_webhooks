import asyncio

from app.app import app
from app.core.config import settings

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
