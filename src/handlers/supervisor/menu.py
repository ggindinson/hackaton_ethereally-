from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from templates import keyboards, texts

menu_router = Router()


@menu_router.callback_query(F.data == "supervisor_menu")
@menu_router.message(F.text == "/supervisor")
async def create_event_handler(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.answer(
            texts.greeting_supervisor,
            reply_markup=keyboards.supervisor_menu_kb(),
        )
    else:
        await event.message.edit_text(
            texts.greeting_supervisor,
            reply_markup=keyboards.supervisor_menu_kb(),
        )
