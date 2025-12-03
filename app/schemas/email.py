from pydantic import BaseModel
from typing import Optional
from app.models.email import EmailStatus
from datetime import datetime

class EmailCreate(BaseModel):
    text_content: Optional[str] = None
    html_content: Optional[str] = None

class EmailResponse(EmailCreate):
    id: int
    status: EmailStatus
    created_at: datetime

    class Config:
        from_attributes = True

class EmailUpdateStatus(BaseModel):
    status: EmailStatus


class EmailUpdate(BaseModel):
    text_content: Optional[str] = None
    html_content: Optional[str] = None
