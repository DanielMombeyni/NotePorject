from sqlalchemy.ext.asyncio import AsyncSession
from app.models import NoteRepository, NoteModel, UserModel, UserRepository
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset
from sqlalchemy import select
from app.infrastructure.service import UserService


__all__ = [
    "provide_note_repo",
    "provide_limit_offset_pagination",
    "provide_note_details_repo",
    "provides_user_service",
]


async def provide_note_repo(db_session: AsyncSession) -> NoteRepository:
    return NoteRepository(session=db_session)


def provide_limit_offset_pagination(
    current_page: int = Parameter(ge=1, query="currentPage", default=1, required=False),
    page_size: int = Parameter(
        query="pageSize",
        ge=1,
        default=10,
        required=False,
    ),
) -> LimitOffset:
    return LimitOffset(page_size, page_size * (current_page - 1))


async def provide_note_details_repo(db_session: AsyncSession) -> NoteRepository:
    return NoteRepository(
        statement=select(NoteModel),
        session=db_session,
    )


# async def provides_user_service(db_session: AsyncSession) -> UserService:
#     async with UserService.new(
#         session=db_session, statement=select(NoteModel)
#     ) as service:
#         yield service


async def provides_user_service(db_session: AsyncSession) -> NoteRepository:
    return UserRepository(
        session=db_session,
    )
