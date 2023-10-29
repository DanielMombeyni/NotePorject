# routers.py
from litestar import Router
from app.controllers import NoteController, UserController

__all__ = ["create_router"]


def create_router(**kwargs) -> Router:
    return Router(
        path="/api/v1",
        route_handlers=[NoteController, UserController],
    )
