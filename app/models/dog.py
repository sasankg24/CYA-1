import uuid
from typing import Optional

from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Dog(Base):
    __tablename__ = "dogs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    age_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    breed: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
