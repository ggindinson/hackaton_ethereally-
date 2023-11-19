from typing import Dict, List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Events
from templates.texts import faq_buttons_mapper, poll_options_mapper


def menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Расписание", callback_data="events")
    builder.button(text="Рейтинг", callback_data="rating")
    builder.button(text="Профориентация", callback_data="poll")
    builder.button(text="Помощь", callback_data="faq")

    builder.adjust(1)
    return builder.as_markup()


def supervisor_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Создать мероприятие", callback_data="create_event")
    builder.button(text="Активные мероприятия", callback_data="get_active_events")

    builder.adjust(1)
    return builder.as_markup()


def events_kb(events: List[Events], user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for event in events:
        user_ids = [user.id for user in event.users]

        if user_id in user_ids:
            additional_data = "✅ "
        else:
            additional_data = ""

        builder.button(
            text=f"{additional_data} {event.name}",
            callback_data=f"event_info|{event.id}",
        )

    builder.button(text="Рекомендации", callback_data="event_recomendations")
    builder.adjust(1)
    build_back_button(builder)
    return builder.as_markup()


def supervisor_events_kb(events: List[Events]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for event in events:
        builder.button(
            text=event.name,
            callback_data=f"supervisor_event_info|{event.id}",
        )

    builder.adjust(1)
    build_back_button(builder, callback_data="supervisor_menu")
    return builder.as_markup()


def supervisor_current_event_kb(event: Events) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Удалить ❌",
        callback_data=f"supervisor_current_event_delete|{event.id}",
    )

    builder.adjust(1)
    build_back_button(builder, callback_data="get_active_events")
    return builder.as_markup()


def current_event_kb(event: Events, user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    user_ids = [user.id for user in event.users]

    if user_id in user_ids:
        builder.button(
            text="Отменить участие ❌",
            callback_data=f"current_event|unsubscribe|{event.id}",
        )
    else:
        builder.button(
            text="Подписаться ✅", callback_data=f"current_event|subscribe|{event.id}"
        )

    builder.adjust(1)
    build_back_button(builder)
    return builder.as_markup()


def faq_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for text, callback_data in faq_buttons_mapper.items():
        builder.button(text=text, callback_data=callback_data)

    build_back_button(builder=builder)

    builder.adjust(1)
    return builder.as_markup()


def poll_options_kb(question_index: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    raw_question: Dict[str, str] = list(poll_options_mapper.values())[question_index]

    for callback_key, text in raw_question.items():
        builder.button(
            text=text, callback_data=f"poll_option|{question_index}|{callback_key}"
        )

    build_back_button(builder=builder)
    builder.adjust(1)
    return builder.as_markup()


def build_back_button(
    builder: InlineKeyboardBuilder | None = None,
    callback_data: str = "main_menu",
    button_text: str = "🔙 Назад",
) -> InlineKeyboardMarkup:
    if not builder:
        builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    return builder.as_markup()


# -------------------------------------- Keyboard mappers -------------------------------------- #
