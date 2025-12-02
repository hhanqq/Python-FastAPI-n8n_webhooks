import logging
from fastapi import FastAPI

from app.core.config import settings
from app.routers import users, auth, admin, emails

def create_app() -> FastAPI:
    """Создание FastAPI приложения"""
    logging.basicConfig(level=settings.LOG_LEVEL)
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    origins = [
        "https://medium-mails.domen1.com/api/",
        "https://medium-mails.domen1.com"
        "http://localhost:5173",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth.router, prefix="/api", tags=["Auth"])
    app.include_router(users.router, prefix="/api", tags=["Users"])
    app.include_router(admin.router, prefix="/api", tags=["Admin"])
    app.include_router(emails.router, prefix="/api", tags=["Emails"])

    return app

app = create_app()
