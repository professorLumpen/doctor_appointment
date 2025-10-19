from datetime import datetime

from pydantic import BaseModel, field_validator


class AppointmentInfo(BaseModel):
    patient_name: str
    office_number: str
    date_time: datetime

    @field_validator("date_time")
    def date_time_must_not_be_none(cls, v):
        if v.tzinfo is not None:
            v = v.replace(tzinfo=None)
        return v
