from fastapi import FastAPI
app =FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/emp/{employee_id}")
def get_employee(employee_id: int):
    return({"id": employee_id, "name": "Jai Sri Krishna"})