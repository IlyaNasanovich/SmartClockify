from datetime import datetime
from uuid import uuid4

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot import form_router
from bot_states import ChatBotState
from mixpanel import log_business_event


@form_router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    await state.set_state(ChatBotState.initialize)
    await message.answer(
        'Hello! Please, send your Clockify API Key.\nGenerate API Key in this URL https://app.clockify.me/user/preferences#advanced and send it here',
        reply_markup=ReplyKeyboardRemove()
    )

    user_data = await state.get_data()
    user_id = user_data['user_id']

    log_business_event('start', {
        'distinct_id': str(user_id),
        '$insert_id': str(uuid4()),
        'time': int(datetime.utcnow().timestamp())
    })
