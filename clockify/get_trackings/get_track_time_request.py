from clockify.get_trackings.get_track_time_model import ClockifyGetTrackTimeData
from clockify.run_clockify_request import get_clockify_request


def get_tracked_time(apikey: str, clockify_user_id: str, workspace_id: str) -> tuple[bool, list[ClockifyGetTrackTimeData]]:
    url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{clockify_user_id}/time-entries'

    response = get_clockify_request(url, apikey)

    if 299 < response.status_code:
        return False, []

    content = response.json()

    return True, [ClockifyGetTrackTimeData(**data) for data in content]
