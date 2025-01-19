from io import BytesIO
from uuid import uuid4

from aiogram.types.voice import Voice
from langchain_core.messages import SystemMessage, HumanMessage

from ai import openai_client, structured_output_model
from bot import bot
from clockify.get_projects.get_projects_request import get_all_projects
from clockify.get_user_info.get_user_info_request import get_user_info
from json import dumps
from pydantic.json import pydantic_encoder
from langchain_community.callbacks.manager import get_openai_callback

from clockify.track_time.track_time_request import ClockifyTrackTimeRequest
from datetime import datetime, date

from mixpanel import log_business_event
from sc_data.repository import save_tracking_times
from pytz import timezone, utc


def handle_time(user_timezone: str, day: str, logged_time: str):
    time_obj = datetime.strptime(logged_time, '%H:%M').time()
    day_obj = datetime.strptime(day, '%Y-%m-%d').date()

    combined_datetime = datetime.combine(day_obj, time_obj)

    user_tz = timezone(user_timezone)
    localized_datetime = user_tz.localize(combined_datetime)

    utc_datetime = localized_datetime.astimezone(utc)

    return utc_datetime.isoformat()


async def track_time_text(message_id: int, trace_id: str, chat_id: int, user_id: int, clockify_apikey: str, message: str) -> str:
    success, user_info = get_user_info(clockify_apikey)

    if not success or user_info is None:
        return 'Failed to get the workspace'

    success, projects = get_all_projects(user_info.active_workspace, clockify_apikey)

    if not success or len(projects) == 0:
        return 'Failed to get the list of projects'

    projects_json = dumps(projects, default=pydantic_encoder)

    prompt = [
        SystemMessage('You are a helpful assistant who must process the user request to track the working time'),
        SystemMessage(f'Here\'s the list of projects of this user: ```json\n{projects_json}\n```'),
        SystemMessage(f'Today is {date.today().isoformat()}'),
        HumanMessage(message)
    ]

    with get_openai_callback() as cb:
        response = await structured_output_model.ainvoke(prompt)

        input_tokens = cb.prompt_tokens
        output_tokens = cb.completion_tokens
        cost_tokens = cb.total_cost

        log_business_event('process_text', {
            'distinct_id': str(user_id),
            '$insert_id': str(uuid4()),
            'time': int(datetime.utcnow().timestamp()),
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost_tokens': cost_tokens,
            'trace_id': trace_id
        })

    res_str = ''

    tracking_times = []

    user_timezone = user_info.settings.time_zone

    for track_time in response.track_times:
        found_project = [project for project in projects if project.id == track_time.project_id][0]

        res_str += f' > {track_time.day_at}. {track_time.start_work_at} - {track_time.end_work_at} [{found_project.name}] {track_time.description}\n'

        body = ClockifyTrackTimeRequest(billable=found_project.billable,
                                        description=track_time.description,
                                        start=handle_time(user_timezone, track_time.day_at, track_time.start_work_at),
                                        end=handle_time(user_timezone, track_time.day_at, track_time.end_work_at),
                                        project_id=found_project.id,
                                        type='REGULAR')

        tracking_times.append(body)

    save_tracking_times(chat_id, user_id, dumps(tracking_times, default=pydantic_encoder), message_id)

    return res_str


async def track_time_voice(message_id: int, trace_id: str, chat_id: int, user_id: int, clockify_apikey: str, voice: Voice) -> str:
    duration_s = voice.duration

    voice_file = await bot.get_file(voice.file_id)
    in_memory_file = BytesIO()
    await bot.download_file(voice_file.file_path, in_memory_file)

    in_memory_file.seek(0)
    in_memory_file.name = voice_file.file_path.split('/')[-1]

    transcription = openai_client.audio.transcriptions.create(
        model='whisper-1',
        file=in_memory_file,
        response_format='text'
    )

    log_business_event('process_voice', {
        'distinct_id': str(user_id),
        '$insert_id': str(uuid4()),
        'time': int(datetime.utcnow().timestamp()),
        'duration': duration_s,
        'trace_id': trace_id
    })

    return await track_time_text(message_id, trace_id, chat_id, user_id, clockify_apikey, transcription)
