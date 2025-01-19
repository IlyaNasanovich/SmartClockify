from pydantic import BaseModel, Field


class ClockifyTrackTimeRequest(BaseModel):
    billable: bool = Field()
    description: str = Field()
    start: str = Field()
    end: str = Field()
    project_id: str = Field(serialization_alias='projectId')
    type: str = Field(default='REGULAR')


class ClockifyTrackTimeResponse(BaseModel):
    id: str = Field()
