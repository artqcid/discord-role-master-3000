"""Router for the /api/channels endpoint."""
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.database import get_db
from backend.repositories.channel_repository import ChannelRepository
from backend.schemas.channel import ChannelResponseSchema

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Channels"])
_repo = ChannelRepository()


@router.get("/channels", response_model=list[ChannelResponseSchema])
async def get_channels(
    session: AsyncSession = Depends(get_db),
) -> list[ChannelResponseSchema]:
    """Return all channels ordered by position."""
    settings = get_settings()
    channels = await _repo.get_all(session, settings.guild_id)
    if not channels:
        raise HTTPException(status_code=404, detail="No channels found. Is the bot synced?")
    return [ChannelResponseSchema.model_validate(c) for c in channels]
