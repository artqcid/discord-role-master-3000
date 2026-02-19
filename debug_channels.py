import asyncio
import os
import sys

# Füge das aktuelle Verzeichnis zum Pfad hinzu
sys.path.append(os.getcwd())

from backend.database import AsyncSessionLocal
from backend.repositories.channel_repository import ChannelRepository
from backend.config import get_settings
from backend.schemas.channel import ChannelResponseSchema

async def main():
    settings = get_settings()
    repo = ChannelRepository()
    print(f"Fetching channels for guild_id: {settings.guild_id}")
    
    async with AsyncSessionLocal() as session:
        try:
            channels = await repo.get_all(session, settings.guild_id)
            print(f"Found {len(channels)} channels.")
            
            for ch in channels:
                try:
                    # Versuche Pydantic Validierung + Serialisierung
                    schema = ChannelResponseSchema.model_validate(ch)
                    json_output = schema.model_dump_json()
                    print(f"  OK (JSON): {len(json_output)} bytes")
                except Exception as e:
                    print(f"  SERIALIZATION ERROR in channel {ch.name}: {e}")
                    import traceback
                    traceback.print_exc()

        except Exception as e:
            print(f"CRASH: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
