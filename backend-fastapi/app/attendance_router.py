from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from datetime import date

from .database import SessionLocal
from .models import Attendance, Employee
from .schemas import AttendanceCreate

router = APIRouter(prefix="/attendance", tags=["Attendance"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/markAttendance")
def markAttendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    try:
        employee = db.query(Employee).filter(Employee.id == attendance.employee_id, Employee.active == True).first()
        if not employee:
            return {"status": False, "message": "Employee not found or inactive", "data": None}

        existing_attendance = db.query(Attendance).filter(
            Attendance.employee_id == attendance.employee_id,
            Attendance.date == attendance.date
        ).first()

        if existing_attendance:
            existing_attendance.status = attendance.status
            db.commit()
            db.refresh(existing_attendance)
            return {
                "status": True,
                "message": "Attendance updated",
                "data": jsonable_encoder(existing_attendance)
            }

        new_attendance = Attendance(**attendance.dict())
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)

        return {
            "status": True,
            "message": "Attendance marked",
            "data": jsonable_encoder(new_attendance)
        }

    except Exception as e:
        return {"status": False, "message": f"Server error: {str(e)}", "data": None}


@router.get("/getEmployeeAttendance/{id}")
def getEmployeeAttendance(id: int, db: Session = Depends(get_db)):
    try:
        employee = db.query(Employee).filter(Employee.id == id, Employee.active == True).first()
        if not employee:
            return {"status": False, "message": "Employee not found or inactive", "data": None}

        attendance_records = db.query(Attendance).filter(Attendance.employee_id == id).order_by(Attendance.date).all()
        return {"status": True, "data": jsonable_encoder(attendance_records)}

    except Exception as e:
        return {"status": False, "message": f"Server error: {str(e)}", "data": None}