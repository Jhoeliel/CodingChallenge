from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    id: int

class JobBase(BaseModel):
    name: str

class JobCreate(JobBase):
    id: int

class EmployeeBase(BaseModel):
    name: str
    hire_date: date
    department_id: int
    job_id: int

class EmployeeCreate(EmployeeBase):
    id: int
