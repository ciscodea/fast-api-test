# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
    )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    class Config:
        """Class only for testing purposes at swagger."""
        schema_extra = {
            "example": {
                "first_name": "Pedro",
                "last_name": "López",
                "age": 24,
                "hair_color": "black",
                "is_married": False
            },
        }


class Location(BaseModel):
    city: str
    state: str
    country: str

    class Config:
        """Class only for testing purposes at swagger."""
        schema_extra = {
            "example": {
                "city": "San Luis Potosí",
                "state": "San Luis Potosí",
                "country": "México",
            }
        }


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
        description="This is the Person name. It's between 1 and 50 chars.",
        example="Pedro"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=26
        )

):
    return {name: age}


# Path Params validaitons.

@app.get("/person/detail/{person_id}")
def show_person_detail(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123
    )
):
    return {person_id: "it exists!"}


# Request Body validations

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the persion ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results