from pydantic import BaseModel as _BaseModel
from uuid import UUID
from dataclasses import dataclass


class BaseModel(_BaseModel):
    model_config = {"from_attributes": True}


class NoteBaseModel(BaseModel):
    id: UUID | None
    title: str
    note: str


class NoteCreate(BaseModel):
    title: str
    note: str


class NoteUpdate(BaseModel):
    title: str | None = None
    note: str | None = None


class AccountRegisterModel(BaseModel):
    username: str
    email: str
    hashed_password: str


@dataclass
class AccountRegister:
    username: str
    email: str
    hashed_password: str


@dataclass
class UserCreate:
    username: str
    email: str
    hashed_password: str
