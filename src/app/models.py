from tortoise import fields
from tortoise.models import Model

class Student(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, description="姓名")
    birthday = fields.DateField(description="生日", null=True)
    gender = fields.CharField(max_length=16, description="性别", null=True)
    sno = fields.IntField(description="学号")
    schoolclass = fields.ForeignKeyField("models.SchoolClass", related_name="students", description="班级", null=True)

    courses = fields.ManyToManyField("models.Course", related_name="students", description="课程")

    # create_at = fields.DatetimeField(auto_now_add=True)
    # update_at = fields.DatetimeField(auto_now=True)


class SchoolClass(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32, description="班级名称")
    scno = fields.IntField(description="班级编号")


class Course(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, description="课程名称")
    credit = fields.IntField(description="学分")
    cno = fields.IntField(description="课程编号")
    teacher = fields.ForeignKeyField("models.Teacher", related_name="courses", description="教师")


class Teacher(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, description="姓名")
    title = fields.CharField(max_length=32, description="职称")
    tno = fields.IntField(description="工号")
    
