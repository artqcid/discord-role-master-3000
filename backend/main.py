"""FastAPI application factory with lifespan, CORS and router registration."""
import asyncio
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
import backend.models  # noqa: F401 – registers all models with Base
from backend.routers import guild, categories, channels, roles, conflicts

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

    from fastapi import Request
    from fastapi.responses import JSONResponse
    import traceback

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        error_msg = f"GLOBAL CRASH: {exc}"
        print(error_msg)
        try:
            with open("global_error.log", "w") as f:
                f.write(error_msg + "\n")
                traceback.print_exc(file=f)
        except Exception:
            pass
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "details": str(exc)},
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(guild.router, prefix="/api")
    app.include_router(categories.router, prefix="/api")
    app.include_router(channels.router, prefix="/api")
    app.include_router(roles.router, prefix="/api")
    app.include_router(conflicts.router, prefix="/api")
    
    print("--- SERVER CONFIGURATION LOADED (Roles Fix Applied) ---")

    @app.get("/api/channels_debug")
    async def debug_channels():
        return [{"id": "debug", "name": "Debug Channel", "type": "text", "position": 0, "nsfw": False}]

    @app.post("/api/shutdown")
    async def shutdown_server():
        """Graceful shutdown endpoint."""
        import os
        import signal
        import threading
        import time

        def kill_later():
            time.sleep(1)
            # Send CTRL_C_EVENT (Windows friendly)
            # Note: This only works if the process has a console window. 
            # In VS Code terminals, it usually works.
            try:
                os.kill(os.getpid(), signal.CTRL_C_EVENT)
            except Exception:
                # Fallback if CTRL_C fails or not on Windows
                os.kill(os.getpid(), signal.SIGTERM)

        # Schedule kill in background so we can return 200 OK first
        threading.Thread(target=kill_later).start()
        return {"message": "Shutting down..."}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8002, reload=True)
