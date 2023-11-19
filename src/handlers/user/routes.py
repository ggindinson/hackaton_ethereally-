from aiogram import Router

from handlers.user.events import events_router
from handlers.user.faq import faq_router
from handlers.user.menu import menu_router
from handlers.user.poll import poll_router
from handlers.user.rating import rating_router

user_router = Router()


user_router.include_routers(
    menu_router,
    events_router,
    rating_router,
    faq_router,
    poll_router,
)
