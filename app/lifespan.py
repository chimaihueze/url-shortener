import logging
from contextlib import asynccontextmanager

from app.core.db.session import init_db, engine


@asynccontextmanager
async def lifespan(app):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    logging.info("Application starting up...")

    try:
        await init_db()
        logging.debug("Database initialized successfully")

        logging.info("Application startup complete")

        yield

    finally:
        logging.debug("Application shutting down...")
        await engine.dispose()
        logging.debug("Database connections closed")
