# note_models.py
from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository


__all__ = ["NoteModel", "NoteRepository"]


class NoteModel(UUIDAuditBase):
    __tablename__ = "NoteTable"
    title: Mapped[str]
    note: Mapped[str]


class NoteRepository(SQLAlchemyAsyncRepository):
    model_type = NoteModel
