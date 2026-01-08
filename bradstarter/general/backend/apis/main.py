from fastapi import APIRouter

from bradstarter.admin.backend.apis import private
from bradstarter.auth.backend.apis import login
from bradstarter.general.backend.apis import utils
from bradstarter.general.backend.components.config import settings
from bradstarter.items.backend.apis import items
from bradstarter.users.backend.apis import users

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
