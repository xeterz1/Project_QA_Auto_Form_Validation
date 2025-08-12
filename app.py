# app.py
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from logic.validations import Name_validation, Email_validation, Age_validation

app = FastAPI()
ROOT = Path(__file__).resolve().parent  # folder where app.py lives

class Form(BaseModel):
    name: str
    email: str
    age: int
    message: str

@app.get("/")
def serve_form():
    return FileResponse(str(ROOT / "form.html"))

@app.post("/submit")
def submit(form: Form):
    try:
        Name_validation(form.name)
        Email_validation(form.email)
        Age_validation(form.age)
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "ok", "message": "Form submitted successfully"}
