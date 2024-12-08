from typing import Optional, Dict, Any, cast

from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType

from bot_states import ChatBotState
from sc_data.repository import delete_fsm_state, insert_fsm_state, get_fsm_state


class SQLiteFsmStorage(BaseStorage):
    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        if state is None:
            delete_fsm_state(key.chat_id, key.user_id)
        else:
            insert_fsm_state(key.chat_id, key.user_id, state.state.split(':')[1])

    async def get_state(self, key: StorageKey) -> Optional[str]:
        value = get_fsm_state(key.chat_id, key.user_id)

        if value is None:
            return None

        return getattr(ChatBotState, value)

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        pass

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        return {
            'user_id': key.user_id,
            'chat_id': key.chat_id
        }

    def __init__(self):
        super().__init__()

    async def close(selfself):
        pass

    async def wait_closed(self):
        pass

    async def reset_data(self, *,
                         chat: int,
                         user: int):
        pass
