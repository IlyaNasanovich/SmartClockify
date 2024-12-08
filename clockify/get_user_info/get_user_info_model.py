from pydantic import BaseModel, Field


class ClockifyUserInfo(BaseModel):
    id: str = Field()
    name: str = Field()
    email: str = Field()
    active_workspace: str = Field(alias="activeWorkspace")
