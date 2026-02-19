"""Pydantic response schema for Category."""
from pydantic import BaseModel


class CategoryResponseSchema(BaseModel):
    """API response model for a Discord channel category."""

    id: str
    name: str
    position: int

    model_config = {"from_attributes": True}
