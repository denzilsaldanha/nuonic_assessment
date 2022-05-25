import sqlalchemy.exc
from fastapi import FastAPI, Depends, status, Query
from pydantic import conlist
from sqlalchemy.orm import Session
from typing import List
from models.database import engine, Base
from fastapi.encoders import jsonable_encoder
from models import models
from schemas.student import StudentBase, StudentUpdate
from schemas.subject import SubjectBase
from models.session import get_database_session
from datetime import datetime

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome. You have come to the Nuonic Python Assessment Page. Move to /docs for futher "
                       "information"}


@app.post("/students", tags=['Students'], status_code=status.HTTP_201_CREATED)
async def add_student(student: StudentBase, db: Session = Depends(get_database_session)):
    student_in = models.Students(**student.dict())
    db.add(student_in)
    db.commit()
    db.refresh(student_in)
    return student_in


@app.patch("/students", tags=['Students'], status_code=status.HTTP_200_OK)
async def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_database_session)):
    student = db.query(models.Students).filter(models.Students.id == student_id).first()
    if not student:
        return 'Student does not exist'
    if student_update.first_name:
        student.first_name = student_update.first_name
    if student_update.address:
        student.address = student_update.address
    if student_update.last_name:
        student.last_name = student_update.last_name
    if student.date_of_birth:
        student.date_of_birth = student_update.date_of_birth
    student.updated_on = datetime.utcnow()
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get('/students', tags=['Students'])
async def get_students(db: Session = Depends(get_database_session)):
    students = db.query(models.Students).all()
    for student in students:
        student.enrollments = db.query(models.Enrollments).filter(models.Enrollments.student_id == student.id).all()
    return students


@app.get('/students/{student_id}', tags=['Students'])
async def get_student(student_id: int, db: Session = Depends(get_database_session)):
    student = db.query(models.Students).filter(models.Students.id == student_id).first()
    if student:
        student.enrollments = db.query(models.Enrollments).filter(models.Enrollments.student_id == student_id).all()
    return student


@app.get('/students/{student_id}/enrollments', tags=['Students'])
async def get_student(student_id: int, db: Session = Depends(get_database_session)):
    return db.query(models.Enrollments).filter(models.Enrollments.student_id == student_id).all()


@app.delete('/students/{student_id}', tags=['Students'], status_code=status.HTTP_200_OK)
async def get_student(student_id: int, db: Session = Depends(get_database_session)):
    student = db.query(models.Students).filter(models.Students.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
    return


@app.post("/subjects", tags=['Subjects'], status_code=status.HTTP_201_CREATED)
async def add_subject(subject: SubjectBase, db: Session = Depends(get_database_session)):
    subject_in = models.Subjects(**subject.dict())
    db.add(subject_in)
    db.commit()
    db.refresh(subject_in)
    return subject_in


@app.patch("/subjects", tags=['Subjects'], status_code=status.HTTP_200_OK)
async def update_subject(subject_id: int, subject_update: SubjectBase, db: Session = Depends(get_database_session)):
    subject = db.query(models.Subjects).filter(models.Subjects.id == subject_id).first()
    if not subject:
        return 'Subject does not exist'
    if subject_update.name:
        subject.name = subject_update.name
    if subject_update.description:
        subject.description = subject_update.description
    subject.updated_on = datetime.utcnow()

    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@app.post("/enrollment", tags=['Enrollment'], status_code=status.HTTP_201_CREATED)
async def add_enrollment(student_id: int, subject_ids: conlist(item_type=int, max_items=100, min_items=0) = Query(None), db: Session = Depends(get_database_session)):
    subject_ids = list(set(subject_ids))
    for subject_id in subject_ids:
        subject = db.query(models.Subjects).filter(models.Subjects.id == subject_id).first()
        if not subject:
            return 'One or more subjects do not exist.'
    student = db.query(models.Students).filter(models.Students.id == student_id).first()
    if not student:
        return 'Student does not exist.'
    for subject_id in subject_ids:
        enrollment = models.Enrollments(student_id=student_id, subject_id=subject_id, complete=False)
        try:
            db.add(enrollment)
            db.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 'One or more Subjects have already been enrolled.'
        db.refresh(enrollment)
    return


@app.patch("/enrollment", tags=['Enrollment'], status_code=status.HTTP_201_CREATED)
async def update_enrollment(student_id: int, complete: bool, subject_id: int, db: Session = Depends(get_database_session)):
    enrollment = db.query(models.Enrollments).filter(models.Enrollments.subject_id == subject_id).filter(
        models.Enrollments.student_id == student_id).first()
    if not enrollment:
        return 'This enrollment does not exist.'
    enrollment.complete = complete
    enrollment.updated_on = datetime.utcnow()
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return


@app.get('/subjects', tags=['Subjects'], )
async def get_subjects(db: Session = Depends(get_database_session)):
    return db.query(models.Subjects).all()


@app.get('/subjects/{subject_id}', tags=['Subjects'], )
async def get_subject(subject_id: int, db: Session = Depends(get_database_session)):
    return db.query(models.Subjects).filter(models.Subjects.id == subject_id).first()


@app.get('/subjects/{subject_id}/students', tags=['Subjects'], )
async def get_subject(subject_id: int, db: Session = Depends(get_database_session)):
    students = db.query(models.Students).join(models.Enrollments,
                                              models.Enrollments.student_id == models.Students.id).filter(
        models.Enrollments.subject_id == subject_id).all()
    return students


Base.metadata.create_all(bind=engine)
