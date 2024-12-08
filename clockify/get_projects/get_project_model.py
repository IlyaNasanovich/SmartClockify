from pydantic import BaseModel, Field


class ClockifyProject(BaseModel):
    id: str = Field()
    name: str = Field()
    billable: bool = Field()
