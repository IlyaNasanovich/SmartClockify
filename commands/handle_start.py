from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot import form_router
from bot_states import ChatBotState


@form_router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    await state.set_state(ChatBotState.initialize)
    await message.answer(
        'Hello! Please, send your Clockify API Key.\nIn Clockify click on your user pic, then Preferences, then switch to Advanced tab, generate API Key and send it here',
        reply_markup=ReplyKeyboardRemove()
    )
