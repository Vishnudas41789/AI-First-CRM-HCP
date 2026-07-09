from pydantic import BaseModel
from datetime import date
from datetime import time


class InteractionCreate(BaseModel):

    hcp_name: str

    interaction_type: str

    interaction_date: date

    interaction_time: time

    attendees: str | None = None

    topics_discussed: str | None = None

    materials_shared: str | None = None

    samples_distributed: str | None = None

    sentiment: str | None = None

    outcome: str | None = None

    follow_up_actions: str | None = None


class InteractionResponse(InteractionCreate):

    id: int

    class Config:
        from_attributes = True