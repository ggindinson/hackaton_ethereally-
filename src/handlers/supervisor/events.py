from typing import List

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Events
from templates import keyboards, texts
from templates.states import CreateEventState
from utils.datetime_utils import format_datetime
from utils.message import MessageUtils

events_router = Router()


@events_router.callback_query(F.data == "create_event")
async def create_event_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        texts.create_event_name,
        reply_markup=keyboards.build_back_button(
            button_text="Отменить создание ❌",
            callback_data="supervisor_menu",
        ),
    )

    await state.set_state(CreateEventState.get_name)
    await state.update_data(msg=MessageUtils.dump(call.message))


@events_router.message(StateFilter(CreateEventState.get_name))
async def create_event_name_handler(message: Message, state: FSMContext):
    await message.delete()
    state_data = await state.get_data()
    msg: Message = MessageUtils.load(state_data["msg"])

    await msg.edit_text(
        texts.create_event_description,
        reply_markup=keyboards.build_back_button(
            button_text="Отменить создание ❌",
            callback_data="supervisor_menu",
        ),
    )

    await state.set_state(CreateEventState.get_description)
    await state.update_data(name=message.text)


@events_router.message(StateFilter(CreateEventState.get_description))
async def create_event_desc_handler(
    message: Message, state: FSMContext, session: AsyncSession
):
    await message.delete()
    state_data = await state.get_data()
    msg: Message = MessageUtils.load(state_data["msg"])

    name: str = state_data["name"]
    description: str = message.text

    await Events.create(
        session=session,
        params={
            "name": name,
            "description": description,
            "creator": message.from_user.id,
        },
    )
    await msg.edit_text(
        texts.success,
        reply_markup=keyboards.build_back_button(callback_data="supervisor_menu"),
    )


@events_router.callback_query(F.data == "get_active_events")
async def active_event_handler(call: CallbackQuery, session: AsyncSession):
    events: List[Events] = await Events.get_all(session=session)

    await call.message.edit_text(
        texts.current_events,
        reply_markup=keyboards.supervisor_events_kb(events),
    )


@events_router.callback_query(F.data.startswith("supervisor_event_info"))
async def current_event_supervisor_handler(
    call: CallbackQuery, session: AsyncSession, callback_data: str
):
    event = await Events.get_by_id(session=session, model_id=int(callback_data))

    await call.message.edit_text(
        f"""<b>Время создания</b> - <code>{format_datetime(event.created_at)}</code>
<b>Создал</b> - <code>{event.creator}</code>
<b>Кол-во участников</b> - <code>{event.users.__len__()}</code>

<b>Описание</b> - <code>{event.description}</code>""",
        reply_markup=keyboards.supervisor_current_event_kb(event),
    )


@events_router.callback_query(F.data.startswith("supervisor_current_event_delete"))
async def delete_event_handler(
    call: CallbackQuery, session: AsyncSession, callback_data: str
):
    await Events.delete(session=session, model_id=int(callback_data))

    return await active_event_handler(call, session)
