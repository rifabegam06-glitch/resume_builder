from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from schemas import EmployeeCreate
from models import Employee, Skill, Project, Personal, Education
from resume_pdf import create_resume
from fastapi.staticfiles import StaticFiles

from db import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@app.post("/employee")
def create_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db)):

    new_employee = Employee(
        name=employee_data.name,
        email=employee_data.email,
        phone=employee_data.phone,
        summary=employee_data.summary
    )
    db.add(new_employee)
    db.commit()
    
    new_personal = Personal(
        employee_id=new_employee.id,
        dob=employee_data.personal.dob,
        gender=employee_data.personal.gender,
        address=employee_data.personal.address
    )
    db.add(new_personal)

    new_education = Education(
        employee_id=new_employee.id,
        degree=employee_data.education.degree,
        institution=employee_data.education.institution,
        year_of_completion=employee_data.education.year_of_completion
    )
    db.add(new_education)

    for skill_data in employee_data.skills:
        new_skill = Skill(
            employee_id=new_employee.id,
            skill_name=skill_data.skill_name
        )
        db.add(new_skill)

    for project_data in employee_data.projects:
        new_project = Project(
            employee_id=new_employee.id,
            project_name=project_data.project_name,
            role=project_data.role,
            description=project_data.description
        )
        db.add(new_project)

    db.commit()
    return {"message": "Employee created successfully"}

@app.get("/resume/{employee_name}")
def generate_resume(employee_name: str, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(
        Employee.name == employee_name
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

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

    pdf_path = create_resume(
        employee,
        personal_info=personal_info,
        education=education,
        skills=skills,
        projects=projects,
    )

    return FileResponse(pdf_path, filename="resume.pdf")

app.mount("/", StaticFiles(directory="static", html=True), name="static")
