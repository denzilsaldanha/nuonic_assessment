from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    date_of_birth: datetime


class StudentUpdate(BaseModel):
    first_name: Optional[str]
    last_name:  Optional[str]
    address:  Optional[str]
    date_of_birth:  Optional[datetime]


class Student(StudentBase):
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True
