from datetime import datetime
from pydantic import BaseModel


class SubjectBase(BaseModel):
    name: str
    description: str


class Subject(SubjectBase):
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True
