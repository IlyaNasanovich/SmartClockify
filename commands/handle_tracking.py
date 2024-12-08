from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot import form_router
from bot_states import ChatBotState
from sc_data.repository import get_apikey, update_clockify_info
from track_time import track_time_voice, track_time_text
from uuid import uuid4


@form_router.message(ChatBotState.tracking)
async def handle_tracking(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()

    chat_id = user_data['chat_id']
    user_id = user_data['user_id']

    apikey = get_apikey(chat_id, user_id)

    if apikey is None:
        await message.answer(
            'Your apikey not found'
        )

        update_clockify_info(chat_id, user_id, apikey='', user_id='', email='', name='')

        await state.set_state(ChatBotState.initialize)

        return

    processing_message = await message.answer(
        'Your request is processing...'
    )
    with_markup = False

    trace_id = str(uuid4())

    if message.text is None and message.voice is not None:
        response = await track_time_voice(processing_message.message_id, trace_id, chat_id, user_id, apikey, message.voice)
        new_text_message = f'Your request is processed. Please, check the info:\n{response}'
        await state.set_state(ChatBotState.confirmation)
        with_markup = True
    elif message.text is not None and message.voice is None:
        response = await track_time_text(processing_message.message_id, trace_id, chat_id, user_id, apikey, message.text)
        new_text_message = f'Your request is processed. Please, check the info:\n{response}'
        await state.set_state(ChatBotState.confirmation)
        with_markup = True
    else:
        new_text_message = 'Invalid message. Please, try again'

    if with_markup:
        confirm_tracking_button = InlineKeyboardButton(text='Confirm', callback_data='confirm')
        not_track_button = InlineKeyboardButton(text='Back', callback_data='back')
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[[confirm_tracking_button, not_track_button]])

        await processing_message.edit_text(new_text_message, reply_markup=inline_kb)
    else:
        await processing_message.edit_text(new_text_message)
