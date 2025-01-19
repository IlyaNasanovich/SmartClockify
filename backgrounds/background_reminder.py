from datetime import datetime
from json import loads
from uuid import uuid4

from mixpanel import log_business_event
from sc_data.repository import get_all_users, get_tracks
from bot import bot


def is_weekend() -> bool:
    today = datetime.now().weekday()
    return today in (5, 6)


async def run_background_reminder():
    print('[run_background_reminder] Start')

    if is_weekend():
        print('[run_background_reminder] End. Today is weekend')
        return

    users = get_all_users()
    today_date = datetime.now().date()

    for user in users:
        chat_id = user['chat_id']
        user_id = user['user_id']

        data = get_tracks(chat_id, user_id)

        records = [] if data is None or data == '' else loads(data)

        track_exists = any(datetime.fromisoformat(record['end']).date() == today_date for record in records)

        if not track_exists:
            log_business_event('reminder', {
                'distinct_id': str(user_id),
                '$insert_id': str(uuid4()),
                'time': int(datetime.utcnow().timestamp())
            })

            await bot.send_message(chat_id, text="Don't forget to track your working time")

    print('[run_background_reminder] End')
