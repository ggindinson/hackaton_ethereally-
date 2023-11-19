from typing import Any, Awaitable, Callable, Dict, List

from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from database.models import Users
from typings.enums import RoleEnum


class AccessRightsMiddleware:
    def __init__(self, rights_allowed: List[RoleEnum]):
        self.rights_allowed = rights_allowed

    @override
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]

        user = await Users.get_by_id(session=session, model_id=event.from_user.id)

        if not user or user.role not in self.rights_allowed:
            return

        return await handler(event, data)
