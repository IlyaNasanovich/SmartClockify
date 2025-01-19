from clockify.run_clockify_request import CLOCKIFY_URL, post_clockify_request
from clockify.track_time.track_time_model import ClockifyTrackTimeRequest, ClockifyTrackTimeResponse


def save_tracked_time(apikey: str, workspace_id: str, body: ClockifyTrackTimeRequest) -> ClockifyTrackTimeResponse | None:
    url = f'{CLOCKIFY_URL}/workspaces/{workspace_id}/time-entries'
    response = post_clockify_request(url, apikey, body)

    if 300 <= response.status_code:
        return None

    return ClockifyTrackTimeResponse(**response.json())
