from datetime import datetime
from json import loads
from uuid import uuid4

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot import form_router, bot
from bot_states import ChatBotState
from aiogram import F

from clockify.get_user_info.get_user_info_request import get_user_info
from clockify.track_time.track_time_model import ClockifyTrackTimeRequest
from clockify.track_time.track_time_request import save_tracked_time
from mixpanel import log_business_event
from save_tracks import cache_track_time
from sc_data.repository import extract_confirmation_info


@form_router.callback_query(ChatBotState.confirmation, F.data.casefold() == 'confirm')
async def handle_removing_tracking(_: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    chat_id = user_data['chat_id']
    user_id = user_data['user_id']

    apikey, data_json, message_id = extract_confirmation_info(chat_id, user_id)

    _, user_info = get_user_info(apikey)

    tracking_times = [ClockifyTrackTimeRequest(**tracking_time) for tracking_time in loads(data_json)]

    for tracking_time in tracking_times:
        res = save_tracked_time(apikey, user_info.active_workspace, tracking_time)

        if res is None:
            log_business_event('failed_to_track_time', {
                'distinct_id': str(user_id),
                '$insert_id': str(uuid4()),
                'time': int(datetime.utcnow().timestamp())
            })
        else:
            track_id = res.id

            cache_track_time(user_id, chat_id, tracking_time.end, track_id)

            log_business_event('track_time', {
                'distinct_id': str(user_id),
                '$insert_id': str(uuid4()),
                'time': int(datetime.utcnow().timestamp()),
                'end_at': tracking_time.end,
                'method': 'smart_clockify',
                'track_id': track_id
            })

    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await bot.send_message(chat_id=chat_id, text='Your info is sent to Clockify\nStart tracking time')

    await state.set_state(ChatBotState.tracking)
