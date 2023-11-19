# Created by https://t.me/vlasovdev private file | Создано https://t.me/vlasovdev private file


from aiogram.filters import BaseFilter
from aiogram.types import Message


class PrivateChatFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private"
