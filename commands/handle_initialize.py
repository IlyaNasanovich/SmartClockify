from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot import form_router
from bot_states import ChatBotState
from clockify.get_user_info.get_user_info_request import get_user_info
from sc_data.repository import update_clockify_info


@form_router.message(ChatBotState.initialize)
async def handle_initialize(message: Message, state: FSMContext) -> None:
    user_api_key = message.text

    success, user_info = get_user_info(user_api_key)

    user_data = await state.get_data()

    chat_id = user_data['chat_id']
    user_id = user_data['user_id']

    if success and user_info is not None:
        clockify_user_id = user_info.id
        user_email = user_info.email
        user_name = user_info.name
        user_timezone = user_info.settings.time_zone

        update_clockify_info(chat_id, user_id, user_api_key, clockify_user_id, user_name, user_email, user_timezone)

        await state.set_state(ChatBotState.tracking)
        await message.answer(
            f'Initialized successfully. You can start tracking your working time.\nExample:\nToday I worked 12:00 to 14:30 on Excel project, I did a big table about our assets\nYou can specify the day, for example, I worked yesterday or 3 days ago',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Delete token')]
                ],
                resize_keyboard=True
            )
        )
    else:
        await message.answer(
            'Your token is invalid.'
        )
