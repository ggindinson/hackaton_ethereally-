from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Users
from filters.general.private import PrivateChatFilter
from templates import keyboards, texts

menu_router = Router()
menu_router.message.filter(PrivateChatFilter())


@menu_router.callback_query(F.data == "main_menu")
@menu_router.message(CommandStart())
async def start_command_handler(
    event: Message | CallbackQuery, session: AsyncSession, state: FSMContext
):
    await state.clear()
    user = await Users.get_by_id(session=session, model_id=event.from_user.id)

    if isinstance(event, Message):
        await event.answer(texts.greeting, reply_markup=keyboards.menu_kb())
    else:
        await event.message.edit_text(texts.greeting, reply_markup=keyboards.menu_kb())

    if not user:
        await Users.create(
            session=session,
            params={
                "id": event.from_user.id,
                "name": event.from_user.first_name,
                "username": event.from_user.username,
            },
        )
