from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.repositories.role_repository import RoleRepository
from backend.config import get_settings

from fastapi import APIRouter
router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("", response_model=list[dict])
async def get_roles(db: AsyncSession = Depends(get_db)):
    """
    Liefert alle Rollen der konfigurierten Guild.
    """
    settings = get_settings()
    repo = RoleRepository()
    roles = await repo.get_all_by_guild(db, settings.guild_id)
    
    return [
        {
            "id": r.id,
            "name": r.name,
            "color": r.color,
            "position": r.position,
            "permissions": r.permissions,
            "managed": r.managed
        }
        for r in roles
    ]


from backend.schemas.role import RoleUpdateSchema, RoleSchema
from fastapi import HTTPException

@router.patch("/{role_id}", response_model=RoleSchema)
async def update_role(
    role_id: str,
    update_data: RoleUpdateSchema,
    db: AsyncSession = Depends(get_db)
):
    """
    Aktualisiert eine Rolle.
    """
    settings = get_settings()
    repo = RoleRepository()
    # Pydantic model to dict, exclude_unset=True to only update provided fields
    data = update_data.model_dump(exclude_unset=True)
    
    updated_role = await repo.update(db, role_id, settings.guild_id, data)
    
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    await db.commit()
    await db.refresh(updated_role)
    
    return updated_role
