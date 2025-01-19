from datetime import datetime
from uuid import uuid4

from clockify.get_trackings.get_track_time_request import get_tracked_time
from clockify.get_user_info.get_user_info_request import get_user_info
from mixpanel import log_business_event
from save_tracks import cache_track_time
from sc_data.repository import get_all_users


async def run_background_check_tracks():
    print('[run_background_check_tracks] Start')

    users = get_all_users()

    for user in users:
        apikey = user['apikey']
        clockify_user_id = user['clockify_user_id']
        chat_id = user['chat_id']
        user_id = user['user_id']

        success, user_info = get_user_info(apikey)

        if not success:
            continue

        success, tracks = get_tracked_time(apikey, clockify_user_id, user_info.active_workspace)

        if not success:
            continue

        for track in tracks:
            track_time = track.time_interval.end
            track_id = track.id

            exist = cache_track_time(user_id, chat_id, track_time, track_id)

            if not exist:
                log_business_event('track_time', {
                    'distinct_id': str(user_id),
                    '$insert_id': str(uuid4()),
                    'time': int(datetime.utcnow().timestamp()),
                    'end_at': track_time,
                    'method': 'manually',
                    'track_id': track_id
                })

    print('[run_background_check_tracks] End')
