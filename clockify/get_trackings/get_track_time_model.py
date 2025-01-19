from pydantic import BaseModel, Field


class ClockifyTimeInterval(BaseModel):
    end: str = Field()


class ClockifyGetTrackTimeData(BaseModel):
    id: str = Field()
    time_interval: ClockifyTimeInterval = Field(alias='timeInterval')
