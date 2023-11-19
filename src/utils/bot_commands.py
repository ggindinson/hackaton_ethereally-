# Created by https://t.me/vlasovdev bot_commands file | Создано https://t.me/vlasovdev bot_commands file


from typing import Dict, List

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeChat
from loguru import logger


async def set_commands(bot: Bot, commands: Dict[str, Dict[str, str]]) -> None:
    formatted_commands = [
        BotCommand(command=comm, description=desc) for comm, desc in commands.items()
    ]
    await bot.set_my_commands(
        commands=formatted_commands,
        scope=BotCommandScope(type="all_private_chats"),
    )
