from aiogram.fsm.state import State, StatesGroup


class ChatBotState(StatesGroup):
    initialize = State()
    tracking = State()
    confirmation = State()
