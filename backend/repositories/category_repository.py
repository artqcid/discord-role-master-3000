"""Repository for Category database operations."""
import logging

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.category import Category

logger = logging.getLogger(__name__)


class CategoryRepository:
    """All DB queries for the Category model."""

    async def upsert_many(
        self, session: AsyncSession, items: list[dict]
    ) -> None:
        """Insert or replace multiple category records."""
        if not items:
            return
        for item in items:
            stmt = insert(Category).values(**item)
            stmt = stmt.on_conflict_do_update(
                index_elements=["id"],
                set_={k: v for k, v in item.items() if k != "id"},
            )
            await session.execute(stmt)
        await session.commit()
        logger.info("Upserted %d categories.", len(items))

    async def get_all(
        self, session: AsyncSession, guild_id: str
    ) -> list[Category]:
        """Return all categories for a guild, ordered by position."""
        result = await session.execute(
            select(Category)
            .where(Category.guild_id == guild_id)
            .order_by(Category.position)
        )
        return list(result.scalars().all())
