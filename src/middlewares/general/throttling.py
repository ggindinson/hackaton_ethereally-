import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import CallbackQuery, Message
from cachetools import TTLCache
from typing_extensions import override


class ThrottlingMiddleware(BaseMiddleware):
    MAX_CACHE_SIZE = 10_000
    DEFAULT_CACHE_TIME: float = 0.4
    GPT_REQUEST_CACHE_TIME: float = 5

    caches: Dict[str, Any] = {
        "gpt_request": TTLCache(maxsize=MAX_CACHE_SIZE, ttl=GPT_REQUEST_CACHE_TIME),
        "default": TTLCache(maxsize=MAX_CACHE_SIZE, ttl=DEFAULT_CACHE_TIME),
    }

    @override
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        throttling_key: str = get_flag(data, "throttling_key", default="default")

        if throttling_key is not None and throttling_key in self.caches:
            if event.from_user.id in self.caches[throttling_key]:
                if isinstance(event, CallbackQuery) or throttling_key != "gpt_request":
                    return

                seconds_before_request = self.GPT_REQUEST_CACHE_TIME - (
                    time.time() - self.caches[throttling_key][event.from_user.id]
                )
                return await event.answer(
                    f"Вы пишите слишком часто!\nПовторите запрос через {seconds_before_request:.0f} сек."
                )
            else:
                self.caches[throttling_key][event.from_user.id] = time.time()
        return await handler(event, data)
