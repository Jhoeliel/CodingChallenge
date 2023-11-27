from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Employee(Base):
    __tablename__ = 'hired_employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hire_date = Column(Date)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))

    # Relaciones (opcional)
    department = relationship("Department")
    job = relationship("Job")
