from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from config.database import Base

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str | None]
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())