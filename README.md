# Coding Challenge
# Section 1: API
In the context of a DB migration with 3 different tables (departments, jobs, employees) , create
a local REST API that must:
1. Receive historical data from CSV files
2. Upload these files to the new DB
3. Be able to insert batch transactions (1 up to 1000 rows) with one request
You need to publish your code in GitHub. It will be taken into account if frequent updates are
made to the repository that allow analyzing the development process. Ideally, create a
markdown file for the Readme.md
Clarifications
● You decide the origin where the CSV files are located.
● You decide the destination database type, but it must be a SQL database.
● The CSV file is comma separated.

# Section 2: SQL
You need to explore the data that was inserted in the previous section. The stakeholders ask
for some specific metrics they need. You should create an end-point for each requirement.
Requirements  <br>
● Number of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job. <br>
● List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending). <br>

# Technology choice:
Language: Python (popular, great support for APIs and data manipulation). <br>
Framework for REST API: FastAPI (modern, fast, with support for asynchronous operations).  <br>
Database: PostgreSQL (robust, widely used in enterprise applications). <br>
ORM (Object-Relational Mapping): SQLAlchemy (facilitates database operations). <br>

# Local Tests
Run the Application: uvicorn app.main:app --reload <br>
http://localhost:8000/docs

# Deploy
Heroku Postgresql
https://desafio1.herokuapp.com/docs <br>
