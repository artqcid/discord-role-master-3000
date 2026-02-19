"""Channel SQLAlchemy model."""
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class Channel(Base):
    """Represents a Discord channel in the database."""

    __tablename__ = "channels"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    guild_id: Mapped[str] = mapped_column(
        String, ForeignKey("guilds.id"), nullable=False
    )
    category_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("categories.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    nsfw: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
