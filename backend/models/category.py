"""Category SQLAlchemy model."""
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class Category(Base):
    """Represents a Discord channel category in the database."""

    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    guild_id: Mapped[str] = mapped_column(
        String, ForeignKey("guilds.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
