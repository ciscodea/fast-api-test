# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Query Params validations.

@app.get("/person/detail")
def show_person_detail(
    name: Optional[str] = Query(
        default=None, 
        min_length=1, 
        max_length=50, 
        title="Person Name", 
        description="This is the Person name. It's between 1 and 50 chars."
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
        )

):
    return {name: age}

# Path Params validaitons.

@app.get("/person/detail/{person_id}")
def show_person_detail(person_id: int = Path(..., gt=0)):
    return {person_id: "it exists!"}
