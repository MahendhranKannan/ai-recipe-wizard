from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    id: int | None = None
    name: str
    age: int
    salary: float | None = 1000.00
    department: str
    is_active: bool = True

@app.post("/employee_deatils/")
def create_employee(emp: Employee):
    return ({"id": 10331, "name": emp.name, "age": emp.age, "salary": emp.salary * 3, "department": emp.department, "is_active": emp.is_active})

@app.get("/{number}")
def square(name: str | None = "Guest", number: int = 0):
    return {"number" : number, "Sqaure": number * number, "Guest" : "Hello" + name}