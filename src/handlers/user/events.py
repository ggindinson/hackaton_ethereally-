from typing import List

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import AssociationTable, Events
from templates import keyboards, texts

events_router = Router()


@events_router.callback_query(F.data == "events")
async def events_handler(call: CallbackQuery, session: AsyncSession):
    events: List[Events] = await Events.get_all(session=session)

    await call.message.edit_text(
        texts.current_events,
        reply_markup=keyboards.events_kb(events, call.from_user.id),
    )


@events_router.callback_query(F.data.startswith("event_info"))
async def event_info_handler(
    call: CallbackQuery, session: AsyncSession, callback_data: str
):
    event = await Events.get_by_id(session=session, model_id=int(callback_data))

    await call.message.edit_text(
        event.description,
        reply_markup=keyboards.current_event_kb(event, call.from_user.id),
    )


@events_router.callback_query(F.data.startswith("current_event"))
async def current_event_handler(
    call: CallbackQuery, session: AsyncSession, callback_data: str
):
    action_type, event_id = callback_data.split("|")
    event_id = int(event_id)

    if action_type == "unsubscribe":
        await AssociationTable.delete_row(session, call.from_user.id, event_id)
    else:
        await AssociationTable.create(
            session, params={"user_id": call.from_user.id, "event_id": event_id}
        )

    return await events_handler(call, session)


@events_router.callback_query(F.data == "events_recommendations")
async def event_recommendation_handler(call: CallbackQuery):
    # TODO Make recommendations
    await call.message.edit_text(
        text=texts.recommendations,
        reply_markup=keyboards.build_back_button(callback_data="events"),
    )
