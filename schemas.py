from pydantic import BaseModel
from typing import  List, Optional
from datetime import datetime, date

class Project(BaseModel):
    project_name: str
    role: str
    description:str

class Skill(BaseModel):
    skill_name: str

class Education(BaseModel):
    degree: str
    institution: str
    year_of_completion: int


class Personal(BaseModel):
    dob: date
    gender: str
    address: str

class EmployeeCreate(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    personal:Personal
    education:Education
    skills:List[Skill]
    projects:List[Project]