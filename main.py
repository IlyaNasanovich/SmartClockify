import asyncio

from aiocron import crontab
from aiogram import Dispatcher

from SQLiteFsmStorage import SQLiteFsmStorage
from bot import form_router, bot
from sc_data.repository import initialize_db
import commands.handle_initialize
import commands.handle_list_projects
import commands.handle_start
import commands.handle_token_removing
import commands.handle_tracking
import commands.handle_remove_tracking
import commands.handle_confirmation
from backgrounds.background_reminder import run_background_reminder
from backgrounds.background_check_tracks import run_background_check_tracks


async def main():
    initialize_db()

    fsm_storage = SQLiteFsmStorage()
    dp = Dispatcher(storage=fsm_storage)
    dp.include_router(form_router)

    print('Bot initialized')

    crontab('*/15 * * * *', func=run_background_check_tracks)
    crontab('0 16 * * *', func=run_background_reminder)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
