from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

print("Current Working Directory:", os.getcwd())
print("Templates folder:", os.listdir("templates"))

from schemas import EmployeeCreate
from models import (
    Employee,
    Personal,
    Education,
    Skill,
    Project,
)

from db import SessionLocal, engine, Base
from resume_pdf import create_resume

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/employees")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        phone=employee.phone,
        summary=employee.summary
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    new_personal = Personal(
        employee_id=new_employee.id,
        dob=employee.personal.dob,
        gender=employee.personal.gender,
        address=employee.personal.address
    )
    db.add(new_personal)

    new_education = Education(
        employee_id=new_employee.id,
        degree=employee.education.degree,
        institution=employee.education.institution,
        year_of_completion=employee.education.year_of_completion
    )
    db.add(new_education)

    for skill_data in employee.skills:
        new_skill = Skill(
            employee_id=new_employee.id,
            skill_name=skill_data.skill_name
        )
        db.add(new_skill)

    for project_data in employee.projects:
        new_project = Project(
            employee_id=new_employee.id,
            project_name=project_data.project_name,
            role=project_data.role,
            description=project_data.description
        )
        db.add(new_project)

    db.commit()

    return {
        "message": "Employee created successfully",
        "employee_id": new_employee.id
    }


@app.get("/resume/{employee_name}")
def generate_resume(
    employee_name: str,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.name == employee_name
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    skills = db.query(Skill).filter(
        Skill.employee_id == employee.id
    ).all()

    projects = db.query(Project).filter(
        Project.employee_id == employee.id
    ).all()

    personal_info = db.query(Personal).filter(
        Personal.employee_id == employee.id
    ).first()

    education = db.query(Education).filter(
        Education.employee_id == employee.id
    ).first()

    # Generate PDF
    pdf_file = create_resume(employee)

    return {
        "message": "Resume generated successfully",
        "pdf_file": pdf_file,
        "employee": employee.name,
        "skills": [skill.skill_name for skill in skills],
        "projects": [project.project_name for project in projects],
        "personal": {
            "dob": personal_info.dob if personal_info else None,
            "gender": personal_info.gender if personal_info else None,
            "address": personal_info.address if personal_info else None,
        },
        "education": {
            "degree": education.degree if education else None,
            "institution": education.institution if education else None,
            "year_of_completion": education.year_of_completion if education else None,
        },
    }


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)