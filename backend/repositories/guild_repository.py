"""Repository for Guild database operations."""
import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.guild import Guild

logger = logging.getLogger(__name__)


class GuildRepository:
    """All DB queries for the Guild model."""

    async def upsert(self, session: AsyncSession, data: dict) -> None:
        """Insert or replace a guild record."""
        data.setdefault("synced_at", datetime.utcnow())
        stmt = insert(Guild).values(**data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={k: v for k, v in data.items() if k != "id"},
        )
        await session.execute(stmt)
        await session.commit()
        logger.info("Upserted guild id=%s", data.get("id"))

    async def get_first(self, session: AsyncSession) -> Guild | None:
        """Return the first guild stored in the database."""
        result = await session.execute(select(Guild).limit(1))
        return result.scalar_one_or_none()
