"""Router for the /api/channels endpoint."""
import logging
import traceback

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


from backend.schemas.permission_overwrite import PermissionOverwriteUpdateSchema

from backend.schemas.permission_overwrite import PermissionOverwriteUpdateSchema

@router.put("/channels/{channel_id}/overwrites/{target_id}")
async def upsert_overwrite(
    channel_id: str,
    target_id: str,
    overwrite_data: PermissionOverwriteUpdateSchema,
    session: AsyncSession = Depends(get_db)
):
    """
    Erstellt oder aktualisiert einen Permission Overwrite für einen Kanal.
    """
    # Validierung: target_type muss 'role' oder 'member' sein
    if overwrite_data.target_type not in ('role', 'member'):
        raise HTTPException(status_code=400, detail="target_type must be 'role' or 'member'")

    await _repo.upsert_overwrite(
        session,
        channel_id,
        target_id,
        overwrite_data.target_type,
        overwrite_data.allow,
        overwrite_data.deny
    )
    await session.commit()
    return {"message": "Overwrite updated"}


@router.delete("/channels/{channel_id}/overwrites/{target_id}")
async def delete_overwrite(
    channel_id: str,
    target_id: str,
    session: AsyncSession = Depends(get_db)
):
    """
    Löscht einen Permission Overwrite.
    """
    await _repo.delete_overwrite(session, channel_id, target_id)
    await session.commit()
    return {"message": "Overwrite deleted"}
