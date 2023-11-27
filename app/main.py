#from fastapi import FastAPI
from typing import List
from .database import engine, SessionLocal
from .models import Base
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from .models import Department, Job, Employee
import pandas as pd
from io import StringIO
from fastapi import FastAPI, HTTPException
from .schemas import DepartmentCreate, JobCreate, EmployeeCreate
from sqlalchemy.orm import Session,func, extract


# Creando las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para crear una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Intenta obtener el primer departamento
        first_department = db.query(Department).first()
        if first_department:
            return {"message": "Conexión exitosa", "first_department": first_department.name}
        return {"message": "Conexión exitosa pero no se encontraron departamentos"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Funciones para procesar y cargar los datos
def process_department_data(df):
    departments = [Department(id=row[0], name=row[1]) for row in df.values]
    return departments

def process_job_data(df):
    jobs = [Job(id=row[0], name=row[1]) for row in df.values]
    return jobs

def process_employee_data(df):
    employees = [Employee(id=row[0], name=row[1], hire_date=row[2], department_id=row[3], job_id=row[4]) for row in df.values]
    return employees

@app.get("/employees-hired-by-quarter")
def get_employees_hired_by_quarter(db: Session = Depends(get_db)):
    results = db.query(
        Department.name, 
        Job.title, 
        extract('quarter', Employee.hire_date).label('quarter'),
        func.count(Employee.id).label('count')
    ).join(Department).join(Job).filter(
        extract('year', Employee.hire_date) == 2021
    ).group_by(
        Department.name, 
        Job.title, 
        'quarter'
    ).order_by(
        Department.name, 
        Job.title
    ).all()

    return results

@app.get("/departments-hiring-above-average")
def get_departments_hiring_above_average(db: Session = Depends(get_db)):
    average_hires = db.query(
        func.avg(func.count(Employee.id)).label('average')
    ).filter(
        extract('year', Employee.hire_date) == 2021
    ).scalar()

    results = db.query(
        Department.id,
        Department.name, 
        func.count(Employee.id).label('count')
    ).join(Employee).filter(
        extract('year', Employee.hire_date) == 2021
    ).group_by(
        Department.id, 
        Department.name
    ).having(
        func.count(Employee.id) > average_hires
    ).order_by(
        func.count(Employee.id).desc()
    ).all()

    return results

# Endpoint para subir y procesar el CSV
@app.post("/upload-csv/{table_name}")
async def upload_csv(table_name: str, file: UploadFile = File(...)):
    session = SessionLocal()
    content = await file.read()
    df = pd.read_csv(StringIO(content.decode('utf-8')), header=None)

    try:
        if table_name == "departments":
            data = process_department_data(df)
        elif table_name == "jobs":
            data = process_job_data(df)
        elif table_name == "hired_employees":
            data = process_employee_data(df)
        else:
            raise HTTPException(status_code=400, detail="Nombre de tabla no válido")

        session.bulk_save_objects(data)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
    
    return {"message": f"Datos cargados con éxito en la tabla {table_name}"}


@app.post("/add-departments")
def add_departments(departments: List[DepartmentCreate]):
    session = SessionLocal()
    try:
        session.bulk_insert_mappings(Department, departments.dict())
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
    return {"message": "Departamentos añadidos con éxito"}

@app.post("/add-jobs")
def add_jobs(jobs: List[JobCreate]):
    session = SessionLocal()
    try:
        session.bulk_insert_mappings(Department, jobs.dict())
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
    return {"message": "Departamentos añadidos con éxito"}

@app.post("/add-employees")
def add_employees(employees: List[EmployeeCreate]):
    session = SessionLocal()
    try:
        session.bulk_insert_mappings(Department, employees.dict())
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
    return {"message": "Departamentos añadidos con éxito"}

