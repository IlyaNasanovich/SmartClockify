from datetime import datetime
from uuid import uuid4

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot import form_router, bot
from bot_states import ChatBotState
from aiogram import F

from mixpanel import log_business_event
from sc_data.repository import extract_confirmation_info


@form_router.callback_query(ChatBotState.confirmation, F.data.casefold() == 'back')
async def handle_removing_tracking(_: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    chat_id = user_data['chat_id']
    user_id = user_data['user_id']

    _, _, message_id = extract_confirmation_info(chat_id, user_id)

    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await bot.send_message(chat_id=chat_id, text='Info is deleted. Start tracking time')

    log_business_event('info_rejection', {
        'distinct_id': str(user_id),
        '$insert_id': str(uuid4()),
        'time': int(datetime.utcnow().timestamp())
    })

    await state.set_state(ChatBotState.tracking)
