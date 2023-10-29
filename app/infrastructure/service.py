# user_service.py
from typing import Any, Coroutine, TypeVar
from pydantic import SecretStr, BaseModel
from app.models import UserModel, UserRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from litestar.exceptions import PermissionDeniedException
from app.infrastructure import crypt
import contextlib
from app.infrastructure.sqlalchemy_plugin import async_session_factory
from collections.abc import Sequence
from litestar.pagination import OffsetPagination
from advanced_alchemy.repository.typing import ModelT
from advanced_alchemy.filters import LimitOffset, FilterTypes
from pydantic.type_adapter import TypeAdapter
from app.controllers.dependencies.schemas import AccountRegisterModel

__all__ = ["UserService"]


ModelDTOT = TypeVar("ModelDTOT", bound="BaseModel")


class UserService(SQLAlchemyAsyncRepositoryService[UserModel]):
    repository_type = UserRepository

    def __init__(self, **repo_kwargs) -> None:
        self.repository: UserRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    def authenticate(self, username, password):
        user_obj = self.get_one_or_none(user_name=username)
        if user_obj is None:
            raise PermissionDeniedException("User not found or password invalid")
        if not crypt.verify_password(password, user_obj.hashed_password):
            raise PermissionDeniedException("User not found or password invalid")
        return user_obj

    async def create(self, data: AccountRegisterModel) -> AccountRegisterModel:
        print("create", UserModel(**data.model_dump()))
        repo = await self.repository.add(
            UserModel(**data.model_dump(exclude_unset=True, exclude_none=True))
        )
        print("repo")
        await self.repository.session.commit()
        return AccountRegisterModel.model_validate(repo)

    async def to_model(
        self, data: UserModel | dict[str, Any], operation: str | None = None
    ) -> UserModel:
        if isinstance(data, dict) and "password" in data:
            password: SecretStr | str | None = data.pop("password", None)
            if password is not None:
                password = (
                    SecretStr(password) if isinstance(password, str) else password
                )
                data.update(
                    {"hashed_password": await crypt.get_password_hash(password)}
                )
        return await super().to_model(data, operation)

    @classmethod
    @contextlib.asynccontextmanager
    async def new(cls, session=None, statement=None):
        if session:
            yield cls(statement=statement, session=session)
        else:
            async with async_session_factory() as db_session:
                yield cls(
                    statement=statement,
                    session=db_session,
                )

    def to_dto(
        self,
        data,
        total=None,
        *filters: FilterTypes,
    ) -> ModelT | OffsetPagination[ModelT]:
        """Convert the object to a format expected by the DTO handler

        Args:
            data: The return from one of the service calls.
            total: the total number of rows in the data
            *filters: Collection route filters.

        Returns:
            The list of instances retrieved from the repository.
        """
        if not isinstance(data, Sequence | list):
            return data
        limit_offset = self.find_filter(LimitOffset, *filters)
        total = total or len(data)
        limit_offset = (
            limit_offset
            if limit_offset is not None
            else LimitOffset(limit=len(data), offset=0)
        )
        return OffsetPagination(
            items=list(data),
            limit=limit_offset.limit,
            offset=limit_offset.offset,
            total=total,
        )

    def to_schema(
        self,
        dto: type[ModelDTOT],
        data: ModelT | Sequence[ModelT],
        total: int | None = None,
        *filters: FilterTypes,
    ) -> ModelDTOT | OffsetPagination[ModelDTOT]:
        """Convert the object to a response schema.

        Args:
            dto: Collection route filters.
            data: The return from one of the service calls.
            total: the total number of rows in the data
            *filters: Collection route filters.

        Returns:
            The list of instances retrieved from the repository.
        """
        if not isinstance(data, Sequence | list):
            return TypeAdapter(dto).validate_python(data)
        limit_offset = self.find_filter(LimitOffset, *filters)
        total = total or len(data)
        limit_offset = (
            limit_offset
            if limit_offset is not None
            else LimitOffset(limit=len(data), offset=0)
        )
        return OffsetPagination[dto](  # type: ignore[valid-type]
            items=TypeAdapter(list[dto]).validate_python(data),  # type: ignore[valid-type]
            limit=limit_offset.limit,
            offset=limit_offset.offset,
            total=total,
        )


# from litestar.contrib.sqlalchemy.repository import ModelT
# from litestar.contrib.repository import AbstractAsyncRepository, FilterTypes

# __all__ = ["Service"]


# class Service:
#     """Implementation all CRUD Services"""

#     def __init__(self, repository) -> None:
#         print("service repo", repository)
#         self.repository = repository

#     async def create(self, data):
#         print(f"in service => {data=}")

#         return await self.repository.add(data)

#     async def list(self, *filters, **kwargs) -> list:
#         return await self.repository.list(*filters, **kwargs)

#     async def update(self, id_, data):
#         return await self.repository.update(data)

#     async def get(self, id_):
#         return await self.repository.get(id_)

#     async def delete(self, id_):
#         return await self.repository.delete(id_)
