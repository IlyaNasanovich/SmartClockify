from pydantic import BaseModel, Field


class TrackTime(BaseModel):
    """Handle a specific track time"""

    project_id: str = Field(description='The id of project for this tracked time')
    description: str = Field(description='What user worked on')
    start_work_at: str = Field(description='When user started to work. Format HH:MM')
    end_work_at: str = Field(description='When user ended to work. Format HH:MM')


class TrackTimeResponse(BaseModel):
    """Handle the list of track times"""

    track_times: list[TrackTime] = Field(description='The list of user\'s tracking times')
