from litestar.contrib.sqlalchemy.plugins.init import SQLAlchemyInitPlugin
from litestar.contrib.sqlalchemy.plugins.init.config import SQLAlchemyAsyncConfig
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from litestar import Litestar
from app.settings import DataBaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine
from typing import cast


__all__ = [
    "async_session_factory",
    "engine",
    "sqlalchemy_config",
    "sqlalchemy_plugin",
    "on_startup",
    "on_shutdown",
]


engine = create_async_engine(
    DataBaseSettings.default_DB_URL,
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


sqlalchemy_config = SQLAlchemyAsyncConfig(
    engine_instance=engine,
    session_maker=async_session_factory,
)

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


def on_startup(app: Litestar):
    if not getattr(app.state, "engine", None):
        app.state.engine = engine
    return cast("AsyncEngine", app.state.engine)


async def on_shutdown(app: Litestar) -> None:
    if getattr(app.state, "engine", None):
        await cast("AsyncEngine", app.state.engine).dispose()
