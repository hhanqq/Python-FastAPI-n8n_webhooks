from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class EmailStatus(enum.Enum):
    ON_APPROVAL = "on_approval"
    APPROVED = "approved"
    EDITED = "edited"
    REJECTED = "rejected"


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    text_content = Column(Text, nullable=False)
    html_content = Column(Text, nullable=False)
    status = Column(Enum(EmailStatus), default=EmailStatus.ON_APPROVAL)
    created_at = Column(DateTime(timezone=True), server_default=func.now())