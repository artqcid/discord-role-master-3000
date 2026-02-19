"""Discord Bot client initialization and event handlers."""
import logging

import discord

from backend.config import get_settings
from backend.bot.sync import initial_sync

logger = logging.getLogger(__name__)

_settings = get_settings()

intents = discord.Intents.default()
intents.guilds = True

_client = discord.Client(intents=intents)


@_client.event
async def on_ready() -> None:
    """Called when the bot has connected and is ready."""
    logger.info("Logged in as %s (id=%s).", _client.user, _client.user.id)
    guild = _client.get_guild(int(_settings.guild_id))
    if guild is None:
        logger.error("Guild id=%s not found. Check GUILD_ID in .env.", _settings.guild_id)
        return
    await initial_sync(guild)


async def start_bot() -> None:
    """Start the Discord bot. Designed to run as an asyncio Task."""
    await _client.start(_settings.discord_bot_token)
