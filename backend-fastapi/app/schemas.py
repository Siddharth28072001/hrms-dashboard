from pydantic import BaseModel
from datetime import date


class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: str
    department: str


class Employee(BaseModel):
    id: int
    employee_id: str
    full_name: str
    email: str
    department: str

    class Config:
        orm_mode = True


class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    status: str


class Attendance(BaseModel):
    id: int
    employee_id: int
    date: date
    status: str

    class Config:
        orm_mode = True