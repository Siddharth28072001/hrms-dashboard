from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .employee_router import router as employee_router
from .attendance_router import router as attendance_router

app = FastAPI(title="HRMS Lite API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router)
app.include_router(attendance_router)