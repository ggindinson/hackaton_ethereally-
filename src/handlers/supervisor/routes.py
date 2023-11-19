from aiogram import Router

from handlers.supervisor.events import events_router
from handlers.supervisor.menu import menu_router
from middlewares.admin.access_rights import AccessRightsMiddleware
from typings.enums import RoleEnum

supervisor_router = Router()

access_middleware_instance = AccessRightsMiddleware(
    rights_allowed=[RoleEnum.SUPERVISOR, RoleEnum.ADMIN]
)
supervisor_router.message.middleware(access_middleware_instance)
supervisor_router.callback_query.middleware(access_middleware_instance)


supervisor_router.include_routers(
    menu_router,
    events_router,
)
