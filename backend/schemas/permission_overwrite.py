"""Pydantic schema for PermissionOverwrite."""
from pydantic import BaseModel


class PermissionOverwriteSchema(BaseModel):
    """API response model for a permission overwrite."""

    id: int
    channel_id: str
    target_id: str
    target_type: str
    allow: str
    deny: str

    model_config = {"from_attributes": True}


class PermissionOverwriteUpdateSchema(BaseModel):
    """Schema for creating or updating an overwrite."""
    target_type: str  # 'role' or 'member'
    allow: str
    deny: str
