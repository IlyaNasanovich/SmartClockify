from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import form_router
from bot_states import ChatBotState
from sc_data.repository import update_clockify_info


@form_router.message(ChatBotState.tracking, F.text.casefold() == 'delete token')
async def handle_token_removing(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()

    chat_id = user_data['chat_id']
    user_id = user_data['user_id']

    update_clockify_info(chat_id, user_id, apikey='', user_id='', email='', name='', user_timezone='')

    await state.set_state(ChatBotState.initialize)
    await message.answer(
        'Your token is removed. Send again your API Key to start tracking time here.'
    )
