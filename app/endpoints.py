from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Appointment
from app.schemas import AppointmentInfo


appointment_router = APIRouter(prefix="/appointment", tags=["appointment"])


@appointment_router.get("/")
async def get_appointments(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Appointment))
    return result.scalars().all()


@appointment_router.post("/")
async def create_appointment(appointment_info: AppointmentInfo, session: AsyncSession = Depends(get_session)):
    appointment = Appointment(**appointment_info.model_dump())
    session.add(appointment)
    await session.commit()
    await session.refresh(appointment)
    return appointment
