import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool
from alembic import context

from app.core.db.declarative_base import Base
from app.model import URL

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(sync_conn):
    context.configure(
        connection=sync_conn,
        target_metadata=target_metadata,
    )
    context.run_migrations()


async def run_migrations_online() -> None:
    engine = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with engine.connect() as conn:
        await conn.run_sync(do_run_migrations)

    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
