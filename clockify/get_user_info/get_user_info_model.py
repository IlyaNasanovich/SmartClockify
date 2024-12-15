from pydantic import BaseModel, Field


class ClockifyUserInfoSetting(BaseModel):
    time_zone: str = Field(alias='timeZone')


class ClockifyUserInfo(BaseModel):
    id: str = Field()
    name: str = Field()
    email: str = Field()
    active_workspace: str = Field(alias="activeWorkspace")
    settings: ClockifyUserInfoSetting = Field()
