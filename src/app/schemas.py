
from tortoise.contrib.pydantic import pydantic_model_creator
from .models import Student, SchoolClass, Course, Teacher # Model imports are fine
from typing import Type, Optional # For type hinting
from pydantic import BaseModel # Pydantic's BaseModel for type hinting

# Define placeholder variables for your schema types
# These will hold the generated Pydantic models once initialized
StudentSchema: Optional[Type[BaseModel]] = None
StudentCreateSchema: Optional[Type[BaseModel]] = None
StudentUpdateSchema: Optional[Type[BaseModel]] = None
SchoolClassSchema: Optional[Type[BaseModel]] = None
SchoolClassCreateSchema: Optional[Type[BaseModel]] = None
SchoolClassUpdateSchema: Optional[Type[BaseModel]] = None
CourseSchema: Optional[Type[BaseModel]] = None
CourseCreateSchema: Optional[Type[BaseModel]] = None
CourseUpdateSchema: Optional[Type[BaseModel]] = None
TeacherSchema: Optional[Type[BaseModel]] = None
TeacherCreateSchema: Optional[Type[BaseModel]] = None
TeacherUpdateSchema: Optional[Type[BaseModel]] = None

def initialize_pydantic_schemas():
    """
    Generates all Pydantic models after Tortoise ORM models are initialized.
    This function MUST be called after Tortoise.init() and Tortoise.generate_schemas().
    """
    global StudentSchema, StudentCreateSchema, StudentUpdateSchema
    global SchoolClassSchema, SchoolClassCreateSchema, SchoolClassUpdateSchema
    global CourseSchema, CourseCreateSchema, CourseUpdateSchema
    global TeacherSchema, TeacherCreateSchema, TeacherUpdateSchema

    print("Initializing Pydantic schemas...")

    StudentSchema = pydantic_model_creator(Student, name="Student")
    StudentCreateSchema = pydantic_model_creator(
        Student,
        name="StudentCreate",
        exclude_readonly=True
    )
    StudentUpdateSchema = pydantic_model_creator(
        Student,
        name="StudentUpdate",
        exclude_readonly=True,
        optional=("name", "birthday", "gender", "sno", "schoolclass_id")
    )

    print("StudentCreateSchema fields:", StudentCreateSchema.__fields__.keys())

    SchoolClassSchema = pydantic_model_creator(SchoolClass, name="SchoolClass")
    SchoolClassCreateSchema = pydantic_model_creator(SchoolClass, name="SchoolClassCreate", exclude_readonly=True)
    SchoolClassUpdateSchema = pydantic_model_creator(
        SchoolClass,
        name="SchoolClassUpdate",
        exclude_readonly=True,
        optional=("name", "scno")
    )

    CourseSchema = pydantic_model_creator(Course, name="Course")
    CourseCreateSchema = pydantic_model_creator(Course, name="CourseCreate", exclude_readonly=True)
    CourseUpdateSchema = pydantic_model_creator(
        Course,
        name="CourseUpdate",
        exclude_readonly=True,
        optional=("name", "credit", "cno", "teacher_id")
    )

    TeacherSchema = pydantic_model_creator(Teacher, name="Teacher")
    TeacherCreateSchema = pydantic_model_creator(Teacher, name="TeacherCreate", exclude_readonly=True)
    TeacherUpdateSchema = pydantic_model_creator(
        Teacher,
        name="TeacherUpdate",
        exclude_readonly=True,
        optional=("name", "title", "tno")
    )
    print("Pydantic schemas initialized.")

