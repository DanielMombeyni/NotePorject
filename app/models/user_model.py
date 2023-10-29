from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from litestar.dto import dto_field
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository


__all__ = ["UserModel", "UserRepository"]


class UserModel(UUIDAuditBase):
    __tablename__ = "user_table"
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(
        String(length=255), info=dto_field("private")
    )


class UserRepository(SQLAlchemyAsyncRepository):
    model_type = UserModel
