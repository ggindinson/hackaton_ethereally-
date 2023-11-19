from aiogram.fsm.state import State, StatesGroup


class CreateEventState(StatesGroup):
    get_name = State()
    get_description = State()


class PollState(StatesGroup):
    get_option = State()
