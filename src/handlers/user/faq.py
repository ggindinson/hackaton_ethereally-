from aiogram import F, Router
from aiogram.types import CallbackQuery

from templates import keyboards, texts

faq_router = Router()


@faq_router.callback_query(F.data == "faq")
async def faq_handler(call: CallbackQuery):
    await call.message.edit_text(
        text=texts.faq_greeting,
        reply_markup=keyboards.faq_kb(),
    )


@faq_router.callback_query(F.data.startswith("faq_question"))
async def faq_question_handler(call: CallbackQuery, callback_data: str):
    await call.message.edit_text(
        text=texts.faq_descriptions_mapper[callback_data],
        reply_markup=keyboards.build_back_button(callback_data="faq"),
    )
