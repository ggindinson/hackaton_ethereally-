from typing import Any, Awaitable, Callable, Dict

from aiogram.types import CallbackQuery, Message
from typing_extensions import override


class CallbackMiddleware:
    @override
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        call: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        try:
            if "|" in call.data:
                callback_data = call.data.split("|", maxsplit=1)[-1]
                data["callback_data"] = callback_data
            return await handler(call, data)
        finally:
            try:
                await call.answer()
            except:
                pass
