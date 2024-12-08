from clockify.get_user_info.get_user_info_model import ClockifyUserInfo
from clockify.run_clockify_request import get_clockify_request, CLOCKIFY_URL


def get_user_info(apikey: str) -> tuple[bool, ClockifyUserInfo | None]:
    url = f'{CLOCKIFY_URL}/user'
    response = get_clockify_request(url, apikey)

    if 299 < response.status_code:
        return False, None

    content = response.json()

    return True, ClockifyUserInfo(**content)
