from litestar.dto import DataclassDTO
from .schemas import AccountRegisterModel, UserCreate
from app.infrastructure import dto
from app.models import UserModel
from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO


# class UserDTO(SQLAlchemyDTO[UserModel]):
#     config = dto.config(
#         exclude={"hashed_password"},
#         max_nested_depth=1,
#     )


# class UserCreateDTO(DataclassDTO[UserCreate]):
#     """User Create."""

#     config = dto.config()


# class AccountRegisterDTO(DataclassDTO[AccountRegisterModel]):
#     """User Account Registration."""

#     config = dto.config()
