from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    created_on =  Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_on = Column(DateTime, default=datetime.utcnow(), nullable=False)


class Subjects(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255),nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_on = Column(DateTime, default=datetime.utcnow(), nullable=False)


class Enrollments(Base):
    __tablename__= 'enrolments'
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    complete = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_on = Column(DateTime, default=datetime.utcnow(), nullable=False)
    __table_args__ = (UniqueConstraint('subject_id', 'student_id', name='_unique_enrollment_constraint'),
                     )