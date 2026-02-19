"""FastAPI application factory with lifespan, CORS and router registration."""
import asyncio
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
import backend.models  # noqa: F401 – registers all models with Base
from backend.routers import guild, categories, channels

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create DB tables and start the Discord bot on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified.")

    from backend.bot.client import start_bot

    bot_task = asyncio.create_task(start_bot())

    yield

    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(title="Discord Role Master 3000", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(guild.router, prefix="/api")
    app.include_router(categories.router, prefix="/api")
    app.include_router(channels.router, prefix="/api")

    return app


app = create_app()
