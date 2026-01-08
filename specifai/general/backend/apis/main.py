from fastapi import APIRouter

from specifai.admin.backend.apis import private
from specifai.auth.backend.apis import login
from specifai.general.backend.apis import utils
from specifai.general.backend.components.config import settings
from specifai.items.backend.apis import items
from specifai.users.backend.apis import users

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
