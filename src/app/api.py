from fastapi import APIRouter, HTTPException
from .models import Student, SchoolClass, Course, Teacher
from .schemas import (
    StudentSchema,
    StudentCreateSchema,
    StudentUpdateSchema,
    SchoolClassSchema,
    SchoolClassCreateSchema,
    SchoolClassUpdateSchema,
    CourseSchema,
    CourseCreateSchema,
    CourseUpdateSchema,
    TeacherSchema,
    TeacherCreateSchema,
    TeacherUpdateSchema,
)

student_router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

@student_router.get('/students')
async def list_students():
    return await Student.all()

@student_router.get('/students/{id}')
async def get_student(id: int):
    result = await Student.get_or_none(id=id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@student_router.post('/students', response_model=StudentSchema)
async def create_student(student: StudentCreateSchema):
    student_data = student.model_dump()
    
    # Handle optional schoolclass
    schoolclass = None
    if student_data.get('schoolclass'):
        class_id = student_data.pop('schoolclass')
        schoolclass = await SchoolClass.get_or_none(id=class_id)
        if not schoolclass:
            raise HTTPException(status_code=404, detail=f"SchoolClass {class_id} not found")
    else:
        # Remove the key if it exists but is None
        student_data.pop('schoolclass', None)

    db_student = await Student.get_or_none(sno=student_data['sno'])
    if db_student:
        raise HTTPException(status_code=400, detail=f"Student {student_data['sno']} already exists")
    
    # Create student with or without schoolclass
    user = await Student.create(**student_data, schoolclass=schoolclass)
    return user

@student_router.patch('/students/{id}', response_model=StudentSchema)
async def update_student_class(id: int, student: StudentUpdateSchema):
    db_student = await Student.get_or_none(id=id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student_data = db_student.model_dump()
    db_student_data.update(student.model_dump(mode='json'))
    class_no = db_student_data.pop('schoolclass')
    schoolclass = await SchoolClass.get_or_none(scno=class_no)
    if not schoolclass:
        raise HTTPException(status_code=404, detail=f"SchoolClass {class_no} not found")
    
    await db_student.save()
    return db_student


@student_router.get('/schoolclasses')
async def list_schoolclasses():
    return await SchoolClass.all()

@student_router.get('/schoolclasses/{id}')
async def get_schoolclass(id: int):
    result = await SchoolClass.get_or_none(id=id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="SchoolClass not found")

@student_router.post('/schoolclasses', response_model=SchoolClassSchema)
async def create_schoolclass(schoolclass: SchoolClassCreateSchema):
    schoolclass_data = schoolclass.model_dump()
    db_schoolclass = await SchoolClass.get_or_none(scno=schoolclass_data['scno'])
    if db_schoolclass:
        raise HTTPException(status_code=400, detail=f"SchoolClass {schoolclass_data['scno']} already exists")
    user = await SchoolClass.create(**schoolclass_data)
    return user
