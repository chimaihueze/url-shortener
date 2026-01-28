import logging
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import DB_NAME
from app.core.db.declarative_base import Base

BASE_DIR = Path(__file__).resolve().parents[3]

DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / str(DB_NAME)

DB_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL must be set")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    )

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Database initialized successfully")

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
