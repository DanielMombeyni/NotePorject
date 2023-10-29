# main.py
from litestar import Litestar
from app.settings import ServerSettings
from typing import Any
from app.routers import create_router
from app.infrastructure.sqlalchemy_plugin import (
    on_shutdown,
    on_startup,
    sqlalchemy_plugin,
)


__all__ = ["create_app"]


def create_app(**kwargs: Any) -> Litestar:
    return Litestar(
        route_handlers=[
            create_router(),
        ],
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
        plugins=[sqlalchemy_plugin],
    )


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=ServerSettings.HOST,
        log_level=ServerSettings.LOG_LEVEL,
        port=ServerSettings.PORT,
        reload=ServerSettings.RELOAD,
        timeout_keep_alive=ServerSettings.KEEPALIVE,
    )
