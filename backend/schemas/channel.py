"""Pydantic response schema for Channel."""
from pydantic import BaseModel


class ChannelResponseSchema(BaseModel):
    """API response model for a Discord channel."""

    id: str
    name: str
    type: str
    position: int
    category_id: str | None = None
    nsfw: bool

    model_config = {"from_attributes": True}
