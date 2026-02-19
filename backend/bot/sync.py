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


from backend.repositories.role_repository import RoleRepository

_guild_repo = GuildRepository()
_cat_repo = CategoryRepository()
_chan_repo = ChannelRepository()
_role_repo = RoleRepository()


def _channel_type_str(channel: discord.abc.GuildChannel) -> str:
    """Map a discord.ChannelType to a human-readable string."""
    return CHANNEL_TYPE_MAP.get(channel.type) or "unknown"


async def initial_sync(guild: discord.Guild) -> None:
    """Sync guild, categories, channels, roles and overwrites into the database."""
    try:
        async with AsyncSessionLocal() as session:
            await _sync_guild(session, guild)
            await _sync_roles(session, guild)
            await _sync_categories(session, guild)
            await _sync_channels(session, guild)
            await _sync_overwrites(session, guild)
            
            await session.commit()
            
    except Exception:
        logger.exception("initial_sync failed")
        raise
    logger.info("initial_sync completed for guild '%s'.", guild.name)


async def _sync_guild(session, guild: discord.Guild) -> None:
    """Persist guild metadata."""
    icon_url = str(guild.icon.url) if guild.icon else None
    await _guild_repo.upsert(
        session,
        {"id": str(guild.id), "name": guild.name, "icon_url": icon_url, "synced_at": datetime.utcnow()},
    )


async def _sync_roles(session, guild: discord.Guild) -> None:
    """Persist guild roles."""
    items = []
    for role in guild.roles:
        items.append({
            "id": str(role.id),
            "guild_id": str(guild.id),
            "name": role.name,
            "color": role.color.value,
            "position": role.position,
            "permissions": str(role.permissions.value),
            "managed": role.managed,
        })
    await _role_repo.upsert_many(session, items)


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


async def _sync_overwrites(session, guild: discord.Guild) -> None:
    """Persist permission overwrites for all channels."""
    items = []
    # Alle Channels (inkl. Kategorien) durchgehen
    all_channels = guild.channels  # beinhaltet Categories, Text, Voice etc.
    
    for channel in all_channels:
        for target, overwrite in channel.overwrites.items():
            # target kann Role oder Member sein
            target_type = "role" if isinstance(target, discord.Role) else "member"
            
            # Allow/Deny Pair to int values
            allow_value = overwrite.pair()[0].value
            deny_value = overwrite.pair()[1].value
            
            items.append({
                "channel_id": str(channel.id),
                "target_id": str(target.id),
                "target_type": target_type,
                "allow": str(allow_value),
                "deny": str(deny_value),
            })
            
    await _chan_repo.upsert_overwrites(session, items)
