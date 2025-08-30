from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.api.v1.router import router as v1_router
from backend.config.settings import get_settings
from backend.database.base import DatabaseManager
from backend.helpers.constants import PUBLIC_API_LIMIT
from backend.helpers.utility import limiter
from backend.middleware.cors import setup_cors
from backend.middleware.logging import LoggingMiddleware, app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    if settings.enable_persistence and settings.database_url:
        global db_manager
        db_manager = DatabaseManager(settings.database_url)
        db_manager.create_tables()
        app_logger.info("Database initialized")

    app_logger.info(f"Starting {settings.app_name}")
    yield

    app_logger.info("Application shutdown")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        root_path="/backend",
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # middleware
    app.add_middleware(LoggingMiddleware, logger=app_logger)
    setup_cors(app)

    # router
    app.include_router(v1_router, prefix=settings.api_v1_prefix)

    @app.get("/", tags=["Main"])
    @limiter.limit(f"{PUBLIC_API_LIMIT}/minute")
    async def root():
        return {"message": f"Welcome to {settings.app_name}"}

    @app.get("/health", tags=["Main"])
    @limiter.limit(f"{PUBLIC_API_LIMIT}/minute")
    async def health_check():
        return {"status": "healthy", "version": "1.0.0"}

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        app_logger.error(f"Global exception: {exc}")
        return JSONResponse(
            status_code=500, content={"message": "Internal server error"}
        )

    return app


# For direct execution
if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "main:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
