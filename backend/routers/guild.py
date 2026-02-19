"""Router for the /api/guild endpoint."""
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.repositories.guild_repository import GuildRepository
from backend.schemas.guild import GuildResponseSchema

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Guild"])
_repo = GuildRepository()


@router.get("/guild", response_model=GuildResponseSchema)
async def get_guild(session: AsyncSession = Depends(get_db)) -> GuildResponseSchema:
    """Return the synced guild information."""
    guild = await _repo.get_first(session)
    if guild is None:
        raise HTTPException(status_code=404, detail="Guild not synced yet.")
    return GuildResponseSchema.model_validate(guild)
