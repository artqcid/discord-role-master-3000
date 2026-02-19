"""Pydantic response schema for Guild."""
from pydantic import BaseModel


class GuildResponseSchema(BaseModel):
    """API response model for a Discord guild."""

    id: str
    name: str
    icon_url: str | None = None

    model_config = {"from_attributes": True}
