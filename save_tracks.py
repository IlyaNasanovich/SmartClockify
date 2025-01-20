from datetime import datetime, timedelta
from json import loads, dumps

from pytz import utc

from sc_data.repository import get_tracks, save_tracks


def cache_track_time(user: int, chat: int, end: str, track_id: str) -> bool:
    data = get_tracks(chat, user)

    records = [] if data is None or data == '' else loads(data)

    track_exists = any(record['track_id'] == track_id for record in records)

    if not track_exists:
        records.append({
            'end': end,
            'track_id': track_id
        })

    current_date = datetime.utcnow()

    records = [
        record for record in records
        if (current_date - timedelta(weeks=10)).replace(tzinfo=utc) <= datetime.fromisoformat(record['end']).replace(tzinfo=utc)
    ]

    save_tracks(dumps(records), chat, user)

    return track_exists
