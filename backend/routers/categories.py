"""Router for the /api/categories endpoint."""
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.database import get_db
from backend.repositories.category_repository import CategoryRepository
from backend.schemas.category import CategoryResponseSchema

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Categories"])
_repo = CategoryRepository()


@router.get("/categories", response_model=list[CategoryResponseSchema])
async def get_categories(
    session: AsyncSession = Depends(get_db),
) -> list[CategoryResponseSchema]:
    """Return all categories ordered by position."""
    settings = get_settings()
    categories = await _repo.get_all(session, settings.guild_id)
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found. Is the bot synced?")
    return [CategoryResponseSchema.model_validate(c) for c in categories]
