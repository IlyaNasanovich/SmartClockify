from clockify.run_clockify_request import CLOCKIFY_URL, post_clockify_request
from clockify.track_time.track_time_model import ClockifyTrackTimeRequest


def save_tracked_time(apikey: str, workspace_id: str, body: ClockifyTrackTimeRequest) -> bool:
    url = f'{CLOCKIFY_URL}/workspaces/{workspace_id}/time-entries'
    response = post_clockify_request(url, apikey, body)

    return response.status_code < 300
