from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import form_router
from bot_states import ChatBotState
from clockify.get_projects.get_projects_request import get_all_projects
from clockify.get_user_info.get_user_info_request import get_user_info
from sc_data.repository import get_apikey, update_clockify_info


@form_router.message(ChatBotState.tracking, F.text.casefold() == 'list of projects')
async def handle_list_projects(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()

    chat_id = user_data['chat_id']
    user_id = user_data['user_id']

    apikey = get_apikey(chat_id, user_id)

    if apikey is None:
        await message.answer(
            'Your apikey not found'
        )

        update_clockify_info(chat_id, user_id, apikey='', user_id='', email='', name='', user_timezone='')

        await state.set_state(ChatBotState.initialize)

        return

    success, user_info = get_user_info(apikey)

    if not success or user_info is None:
        await message.answer(
            'Failed to get the workspace'
        )

        return

    success, projects = get_all_projects(user_info.active_workspace, apikey)

    if not success or len(projects) == 0:
        await message.answer(
            'Failed to get the list of projects'
        )

        return

    list_of_projects = '\n'.join([f'* {project.name}' for project in projects])

    await message.answer(
        f'Your assigned projects:\n{list_of_projects}'
    )
