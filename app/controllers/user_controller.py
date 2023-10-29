# user_controller.py
from litestar import Controller, MediaType, Response, get, post
from litestar.di import Provide
from app.controllers.dependencies.providers import provides_user_service
from app.infrastructure.service import UserService
from app.models import UserModel, UserRepository
from app.controllers.dependencies.schemas import AccountRegisterModel



class UserController(Controller):
    """User login and registration."""

    path = "/auth/"
    tags = ["Authenticate"]
    dependencies = {"users_service": Provide(provides_user_service)}
    signature_namespace = {"UserService": UserRepository, "UserModel": UserModel}

    @post("/register")
    async def signup(
        self, users_service: UserRepository, data: AccountRegisterModel
    ) -> AccountRegisterModel:
        obj = await users_service.add(
            UserModel(**data.model_dump(exclude_unset=True, exclude_none=True))
        )
        await users_service.session.commit()
        return AccountRegisterModel.model_validate(obj)
