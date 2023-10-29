# note_controller.py
from litestar import Controller, delete, get, post, patch, put
from app.models import NoteModel, NoteRepository
from litestar.di import Provide
from app.controllers.dependencies import (
    provide_note_repo,
    provide_limit_offset_pagination,
    provide_note_details_repo,
    NoteBaseModel,
    NoteCreate,
    NoteUpdate,
)
from pydantic import TypeAdapter
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset
from litestar.params import Parameter
from uuid import UUID

__all__ = ["NoteController"]


DETAIL_ROUTE = "/{note_id:uuid}"


class NoteController(Controller):
    tags = ["Note"]
    path = "/notes/"
    dependencies = {
        "notes_repo": Provide(provide_note_repo),
    }

    @get(
        dependencies={
            "limit_offset": Provide(
                provide_limit_offset_pagination, sync_to_thread=False
            )
        }
    )
    async def list_notes(
        self,
        notes_repo: NoteRepository,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[NoteBaseModel]:
        """Get a list of notes."""

        results, total = await notes_repo.list_and_count(limit_offset)
        type_adapter = TypeAdapter(list[NoteBaseModel])
        return OffsetPagination[NoteBaseModel](
            items=type_adapter.validate_python(results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @get(f"{DETAIL_ROUTE}")
    async def get_note(
        self, notes_repo: NoteRepository, note_id: UUID
    ) -> NoteBaseModel:
        note = await notes_repo.get(note_id)
        return NoteBaseModel.model_validate(note)

    @post()
    async def create_note(
        self, notes_repo: NoteRepository, data: NoteCreate
    ) -> NoteBaseModel:
        """Create an `Note`."""

        obj = await notes_repo.add(
            NoteModel(**data.model_dump(exclude_unset=True, exclude_none=True))
        )
        await notes_repo.session.commit()
        return NoteBaseModel.model_validate(obj)

    @delete(path=f"/{DETAIL_ROUTE}")
    async def delete_note(
        self,
        notes_repo: NoteRepository,
        note_id: UUID = Parameter(
            title="Note ID",
            description="The Note to delete.",
        ),
    ) -> None:
        """Delete a note from the DB."""
        _ = await notes_repo.delete(note_id)
        await notes_repo.session.commit()

    @patch(
        f"{DETAIL_ROUTE}",
        dependencies={"notes_repo": Provide(provide_note_details_repo)},
    )
    async def update_note(
        self,
        notes_repo: NoteRepository,
        data: NoteUpdate,
        note_id: UUID = Parameter(
            title="Note ID",
            description="The Note to update.",
        ),
    ) -> NoteBaseModel:
        raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
        raw_obj.update({"id": note_id})
        note = await notes_repo.update(NoteModel(**raw_obj))
        await notes_repo.session.commit()
        return NoteBaseModel.model_validate(note)
