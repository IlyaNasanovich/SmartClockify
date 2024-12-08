from requests import post
from config import MIXPANEL_PROJECT_ID, MIXPANEL_AUTH_TOKEN


def log_business_event(event_name: str, data: dict[str, any]) -> bool:
    url = f'https://api-eu.mixpanel.com/import?strict=1&project_id={MIXPANEL_PROJECT_ID}'

    response = post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Basic {MIXPANEL_AUTH_TOKEN}'
    }, json=[{
        'event': event_name,
        'properties': data
    }])

    return response.status_code < 300
