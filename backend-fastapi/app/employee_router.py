from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from .database import SessionLocal
from .models import Employee
from .schemas import EmployeeCreate

import re

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/addEmployee")
def addEmployee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, employee.email):
            return {"status": False, "message": "Invalid email format", "data": None}

        employee_id_upper = employee.employee_id.upper()

        existing_emp = (
            db.query(Employee)
            .filter(Employee.employee_id == employee_id_upper, Employee.active == True)
            .first()
        )
        if existing_emp:
            return {"status": False, "message": "Employee ID already exists", "data": None}

        existing_email = (
            db.query(Employee)
            .filter(Employee.email == employee.email, Employee.active == True)
            .first()
        )
        if existing_email:
            return {"status": False, "message": "Email already registered", "data": None}

        employee_data = employee.dict()
        employee_data["employee_id"] = employee_id_upper
        employee_data["active"] = True
        new_employee = Employee(**employee_data)

        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return {
            "status": True,
            "message": "Employee created successfully",
            "data": jsonable_encoder(new_employee),  # ensure JSON safe
        }

    except Exception as e:
        return {"status": False, "message": f"Server error: {str(e)}", "data": None}


@router.get("/getEmployeeList")
def getEmployees(db: Session = Depends(get_db)):
    try:
        employees = db.query(Employee).filter(Employee.active == True).all()
        return {"status": True, "data": jsonable_encoder(employees)}
    except Exception as e:
        return {"status": False, "message": f"Server error: {str(e)}", "data": None}


@router.delete("/deleteEmployee/{id}")
def deleteEmployee(id: int, db: Session = Depends(get_db)):
    try:
        employee = (
            db.query(Employee)
            .filter(Employee.id == id, Employee.active == True)
            .first()
        )
        if not employee:
            return {
                "status": False,
                "message": "Employee not found or already deleted",
                "data": None,
            }

        employee.active = False
        db.commit()

        return {"status": True, "message": "Employee deleted successfully", "data": None}

    except Exception as e:
        return {"status": False, "message": f"Server error: {str(e)}", "data": None}