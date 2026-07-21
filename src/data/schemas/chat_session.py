"""ORM model for the ``chat_sessions`` table."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.schemas.base import SQLAlchemyBase

if TYPE_CHECKING:
    from data.schemas.user import User


class ChatSession(SQLAlchemyBase):
    """ORM representation of the ``chat_sessions`` table.

    Attributes:
        id (UUID): Primary key, auto-generated via ``uuid4``.
        user_id (UUID): Foreign key linking to ``users.id``.
        title (str): Title of the chat session, max 255 characters.
        user (User): Many-to-one relationship back to the ``User`` model.
    """

    __tablename__ = "chat_sessions"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="chat_sessions",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=E1102
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),  # pylint: disable=E1102
        nullable=True,
    )
