from fastapi import FastAPI

from app.endpoints import appointment_router


app = FastAPI()
app.include_router(appointment_router)
