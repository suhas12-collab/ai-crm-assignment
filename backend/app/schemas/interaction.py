from datetime import date, time
from pydantic import BaseModel


class InteractionCreate(BaseModel):
    doctor_name: str
    hospital: str
    interaction_type: str
    interaction_date: date
    interaction_time: time
    discussion: str
    follow_up: str


class InteractionResponse(InteractionCreate):
    id: int

    class Config:
        from_attributes = True