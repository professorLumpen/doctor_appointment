from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped

from app.db import Base


class Appointment(Base):
    __tablename__ = "appointment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_name: Mapped[str]
    office_number: Mapped[str]
    date_time: Mapped[datetime]
