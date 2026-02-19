from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from backend.models.role import Role

class RoleRepository:
    @staticmethod
    async def upsert_many(session: AsyncSession, roles_data: list[dict]):
        if not roles_data:
            return

        stmt = sqlite_insert(Role).values(roles_data)
        
        # Upsert-Logik für SQLite (ON CONFLICT DO UPDATE)
        update_dict = {
            col.name: col
            for col in stmt.excluded
            if col.name != 'id' and col.name != 'guild_id'
        }
        
        if update_dict:
            stmt = stmt.on_conflict_do_update(
                index_elements=['id'],
                set_=update_dict
            )
        else:
            stmt = stmt.on_conflict_do_nothing(index_elements=['id'])

        await session.execute(stmt)

    @staticmethod
    async def get_all_by_guild(session: AsyncSession, guild_id: str) -> list[Role]:
        stmt = select(Role).where(Role.guild_id == guild_id).order_by(Role.position.desc())
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update(session: AsyncSession, role_id: str, guild_id: str, update_data: dict) -> Role | None:
        """Updates a role with the given data."""
        stmt = select(Role).where(Role.id == role_id, Role.guild_id == guild_id)
        result = await session.execute(stmt)
        role = result.scalars().first()
        
        if not role:
            return None
            
        for key, value in update_data.items():
            if value is not None:
                setattr(role, key, value)
        
        return role
