"""Discord Bot sync logic – initial_sync writes guild data to the database."""
import logging
from datetime import datetime

import discord

from backend.database import AsyncSessionLocal
from backend.repositories.category_repository import CategoryRepository
from backend.repositories.channel_repository import ChannelRepository
from backend.repositories.guild_repository import GuildRepository

logger = logging.getLogger(__name__)

CHANNEL_TYPE_MAP = {
    discord.ChannelType.text: "text",
    discord.ChannelType.voice: "voice",
    discord.ChannelType.forum: "forum",
    discord.ChannelType.stage_voice: "stage",
    discord.ChannelType.news: "announcement",
}

_guild_repo = GuildRepository()
_cat_repo = CategoryRepository()
_chan_repo = ChannelRepository()


def _channel_type_str(channel: discord.abc.GuildChannel) -> str:
    """Map a discord.ChannelType to a human-readable string."""
    return CHANNEL_TYPE_MAP.get(channel.type, "unknown")


async def initial_sync(guild: discord.Guild) -> None:
    """Sync guild, categories and channels into the database."""
    async with AsyncSessionLocal() as session:
        await _sync_guild(session, guild)
        await _sync_categories(session, guild)
        await _sync_channels(session, guild)
    logger.info("initial_sync completed for guild '%s'.", guild.name)


async def _sync_guild(session, guild: discord.Guild) -> None:
    """Persist guild metadata."""
    icon_url = str(guild.icon.url) if guild.icon else None
    await _guild_repo.upsert(
        session,
        {"id": str(guild.id), "name": guild.name, "icon_url": icon_url, "synced_at": datetime.utcnow()},
    )


async def _sync_categories(session, guild: discord.Guild) -> None:
    """Persist all channel categories."""
    items = [
        {"id": str(cat.id), "guild_id": str(guild.id), "name": cat.name, "position": cat.position}
        for cat in guild.categories
    ]
    await _cat_repo.upsert_many(session, items)


async def _sync_channels(session, guild: discord.Guild) -> None:
    """Persist all non-category channels."""
    items = [
        {
            "id": str(ch.id),
            "guild_id": str(guild.id),
            "category_id": str(ch.category_id) if ch.category_id else None,
            "name": ch.name,
            "type": _channel_type_str(ch),
            "position": ch.position,
            "nsfw": getattr(ch, "nsfw", False),
        }
        for ch in guild.channels
        if not isinstance(ch, discord.CategoryChannel)
    ]
    await _chan_repo.upsert_many(session, items)
