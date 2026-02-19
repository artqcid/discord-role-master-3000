"""Repository for Channel database operations."""
import logging

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.channel import Channel

logger = logging.getLogger(__name__)


class ChannelRepository:
    """All DB queries for the Channel model."""

    async def upsert_many(
        self, session: AsyncSession, items: list[dict]
    ) -> None:
        """Insert or replace multiple channel records."""
        if not items:
            return
        for item in items:
            stmt = insert(Channel).values(**item)
            stmt = stmt.on_conflict_do_update(
                index_elements=["id"],
                set_={k: v for k, v in item.items() if k != "id"},
            )
            await session.execute(stmt)
        await session.commit()
        logger.info("Upserted %d channels.", len(items))

    async def get_all(
        self, session: AsyncSession, guild_id: str
    ) -> list[Channel]:
        """Return all channels for a guild, ordered by position."""
        result = await session.execute(
            select(Channel)
            .where(Channel.guild_id == guild_id)
            .order_by(Channel.position)
        )
        return list(result.scalars().all())
