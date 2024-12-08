from typing import Optional

from sc_data.database import execute_query, get_one


def initialize_db():
    with open('./sc_data/queries/initialize.sql') as file:
        execute_query(file.read())


def delete_fsm_state(chat: int, user: int):
    with open('./sc_data/queries/delete_state.sql') as file:
        execute_query(file.read(), (chat, user))


def insert_fsm_state(chat: int, user: int, state: Optional[str]):
    with open('./sc_data/queries/insert_state.sql') as file:
        execute_query(file.read(), (chat, user, state, state))


def get_fsm_state(chat: int, user: int):
    with open('./sc_data/queries/get_state.sql') as file:
        value = get_one(file.read(), (chat, user))
        return value[0] if value else None


def update_clockify_info(chat: int, user: int, apikey: str, user_id: str, name: str, email: str):
    with open('./sc_data/queries/save_clockify_info.sql') as file:
        execute_query(file.read(), (apikey, user_id, name, email, chat, user))


def get_apikey(chat: int, user: int):
    with open('./sc_data/queries/get_apikey.sql') as file:
        value = get_one(file.read(), (chat, user))
        return value[0] if value else None


def save_tracking_times(chat: int, user: int, tracks_json: str, message_id: int):
    with open('./sc_data/queries/save_tracking.sql') as file:
        execute_query(file.read(), (tracks_json, message_id, chat, user))


def extract_confirmation_info(chat: int, user: int):
    with open('./sc_data/queries/extract_confirmation_info.sql') as file:
        value = get_one(file.read(), (chat, user))

        if value is None:
            return None, None, None
        return value[0], value[1], value[2]
