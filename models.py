from sqlalchemy import Column, Date, ForeignKey, Integer, String,Text
from db import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    summary = Column(Text)
    

class Personal(Base):
    __tablename__ = "personal_info"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    dob = Column(Date)
    gender = Column(String)
    address = Column(String)

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    degree = Column(String)
    institution = Column(String)
    year_of_completion = Column(Integer)

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    skill_name = Column(String)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    project_name = Column(String)
    role = Column(String)
    description = Column(Text)             
    