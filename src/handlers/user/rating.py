from typing import List

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Users
from templates import keyboards, texts

rating_router = Router()


@rating_router.callback_query(F.data == "rating")
async def rating_handler(call: CallbackQuery, session: AsyncSession):
    users_rating: List[Users] = await Users.get_rating(session=session)

    await call.message.edit_text(
        texts.rating(users_rating=users_rating),
        reply_markup=keyboards.build_back_button(),
        disable_web_page_preview=True,
    )
