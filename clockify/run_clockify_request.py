from pydantic import BaseModel
from requests import get, post


CLOCKIFY_URL = 'https://api.clockify.me/api/v1'


def get_clockify_request(url: str, apikey: str):
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': apikey
    }

    return get(url, headers=headers)


def post_clockify_request(url: str, apikey: str, content: BaseModel):
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': apikey
    }

    return post(url, headers=headers, data=content.json(by_alias=True))
