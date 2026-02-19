"""Pydantic schema for Role."""
from pydantic import BaseModel


class RoleSchema(BaseModel):
    """API response model for a Discord role."""

    id: str
    name: str
    color: int
    position: int
    permissions: str
    managed: bool
    guild_id: str

    model_config = {"from_attributes": True}


class RoleUpdateSchema(BaseModel):
    """Schema for updating a role."""
    name: str | None = None
    color: int | None = None
    position: int | None = None
    permissions: str | None = None
    managed: bool | None = None
