import logging
from contextlib import suppress
from typing import Any, Dict

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.db_utils import create_engine, create_session, create_tables
from handlers.supervisor.routes import supervisor_router
from handlers.user.routes import user_router
from middlewares.general.callback import CallbackMiddleware
from middlewares.general.db_middleware import DbSessionMiddleware
from middlewares.general.throttling import ThrottlingMiddleware
from settings import settings
from typings.consts import COMMANDS, DEBUG_MODE
from utils.bot_commands import set_commands
from utils.loguru_handler import LoguruHandler


async def on_startup(
    bot: Bot,
    dp: Dispatcher,
    scheduler: AsyncIOScheduler,
):
    if settings.webhook:
        await bot.set_webhook(
            f"{settings.webhook.base_url}{settings.webhook.path}",
            allowed_updates=dp.resolve_used_update_types(),
            max_connections=40,
            drop_pending_updates=True,
        )
    else:
        await bot.delete_webhook(drop_pending_updates=True)
    # Notify & set commands
    await set_commands(bot=bot, commands=COMMANDS)

    # Create tables if they don't exist
    await create_tables(create_engine())

    scheduler.start()


def init_scheduler(bot: Bot, sessionmaker: async_sessionmaker[AsyncSession]):
    # Create scheduler & attach cron tasks
    scheduler = AsyncIOScheduler(
        executors={"default": AsyncIOExecutor()},
    )

    return scheduler


def init_logger():
    # Configure logger
    logging.basicConfig(handlers=[LoguruHandler()], level=logging.INFO, force=True)
    if not DEBUG_MODE:
        pass
        logger.disable("aiohttp.web_log")
        logger.disable("apscheduler.executors")
    logger.warning("Give us the highest rate, please 💖")


def init_dispatcher(sessionmaker: async_sessionmaker[AsyncSession]) -> Dispatcher:
    # Main storage, which will be used in Dispatcher
    storage = RedisStorage.from_url(settings.redis_dsn, connection_kwargs={"db": 1})

    dp = Dispatcher(storage=storage)
    dp.include_routers(
        user_router,
        supervisor_router,
    )
    dp.update.middleware(DbSessionMiddleware(sessionmaker=sessionmaker))
    dp.callback_query.middleware(CallbackMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

    dp.startup.register(on_startup)
    return dp


def main():
    # Initialize Bot
    bot = Bot(settings.bot_token, parse_mode="HTML")

    # Initialise engine and sessionmaker
    engine = create_engine()
    sessionmaker = create_session(engine=engine)

    # Initialise scheduler
    scheduler = init_scheduler(bot, sessionmaker)

    # Initialize logger
    init_logger()

    # Initialize Dispatcher and connect routers & middlewares
    dp = init_dispatcher(sessionmaker)

    # Initialize bot context
    bot_context: Dict[str, Any] = {
        "sessionmaker": sessionmaker,
        "scheduler": scheduler,
        "dp": dp,
    }

    if settings.webhook:
        app = web.Application()
        app["bot"] = bot

        SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            **bot_context,
        ).register(app, path=settings.webhook.path)

        setup_application(
            app,
            dp,
            bot=bot,
            **bot_context,
        )
        web.run_app(
            app,
            host=settings.webhook.webserver_host,
            port=settings.webhook.webserver_port,
        )

    else:
        dp.run_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            **bot_context,
        )


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        main()
