from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from templates import keyboards, texts
from templates.states import PollState

poll_router = Router()


@poll_router.callback_query(F.data.startswith("poll"))
async def poll_handler(
    call: CallbackQuery,
    state: FSMContext,
    callback_data: str = "0|0",
):
    current_question_index, choice_index = callback_data.split("|")
    current_question_index = int(current_question_index)
    state_data = await state.get_data()

    if current_question_index > 0:
        if choice_index != "0":
            current_key_value = state_data[choice_index]
            await state.update_data({choice_index: current_key_value + 1})
    else:
        await state.set_state(PollState.get_option)
        await state.set_data(
            {key: 0 for key in ("a", "b", "c", "d", "e")},
        )

    if current_question_index == len(texts.poll_options_mapper.keys()) - 1:
        max_key = max(state_data, key=state_data.get)
        raw_result = texts.poll_results_mapper[max_key]

        await state.clear()
        return await call.message.edit_text(
            texts.poll_result(raw_result), reply_markup=keyboards.build_back_button()
        )

    question_text = list(texts.poll_options_mapper.keys())[current_question_index + 1]

    await call.message.edit_text(
        f"<i><b>{question_text}</b></i>",
        reply_markup=keyboards.poll_options_kb(
            question_index=current_question_index + 1
        ),
    )
