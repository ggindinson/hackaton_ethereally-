from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Users
from typings.enums import RoleEnum


class AccessRoleFilter(BaseFilter):
    def __init__(self, role_values: List[RoleEnum], session: AsyncSession):
        self.role_values = role_values
        self.session = session

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = await Users.get_by_id(session=self.session, model_id=event.from_user.id)

        return user.role in self.role_values
