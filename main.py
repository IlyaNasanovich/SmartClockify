import asyncio

from aiogram import Dispatcher

from SQLiteFsmStorage import SQLiteFsmStorage
from bot import form_router, bot
from sc_data.repository import initialize_db
import commands.handle_initialize
import commands.handle_start
import commands.handle_token_removing
import commands.handle_tracking
import commands.handle_remove_tracking
import commands.handle_confirmation


async def main():
    initialize_db()

    fsm_storage = SQLiteFsmStorage()
    dp = Dispatcher(storage=fsm_storage)
    dp.include_router(form_router)

    print('Bot initialized')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
