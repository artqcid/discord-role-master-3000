"""Router for conflict detection."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.repositories.channel_repository import ChannelRepository
from backend.repositories.role_repository import RoleRepository
from backend.services.permission_calculator import PermissionCalculator
from backend.config import get_settings

router = APIRouter(prefix="/conflicts", tags=["Conflicts"])

@router.get("")
async def get_conflicts(session: AsyncSession = Depends(get_db)):
    """
    Detects permission conflicts across the guild.
    """
    settings = get_settings()
    guild_id = settings.guild_id
    
    # Load all data
    channel_repo = ChannelRepository()
    role_repo = RoleRepository()
    
    channels = await channel_repo.get_all(session, guild_id)
    roles = await role_repo.get_all_by_guild(session, guild_id)
    
    all_conflicts = []
    
    for channel in channels:
        for role in roles:
            # We only care about role overwrites here
            conflicts = PermissionCalculator.detect_conflicts(channel, role)
            for c in conflicts:
                # Add human readable permission name
                c["permission_name"] = PermissionCalculator.explain_permission(c["permission_bit"])
                c["channel_name"] = channel.name
                c["role_name"] = role.name
                all_conflicts.append(c)
                
    return all_conflicts
