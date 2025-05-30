from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "schoolclass" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(32) NOT NULL,
    "grade" INT NOT NULL,
    "scno" INT NOT NULL
);
COMMENT ON COLUMN "schoolclass"."name" IS '班级名称';
COMMENT ON COLUMN "schoolclass"."grade" IS '年级';
COMMENT ON COLUMN "schoolclass"."scno" IS '班级编号';
CREATE TABLE IF NOT EXISTS "student" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "birthday" DATE,
    "gender" VARCHAR(16),
    "sno" INT NOT NULL,
    "schoolclass_id" INT NOT NULL REFERENCES "schoolclass" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "student"."name" IS '姓名';
COMMENT ON COLUMN "student"."birthday" IS '生日';
COMMENT ON COLUMN "student"."gender" IS '性别';
COMMENT ON COLUMN "student"."sno" IS '学号';
COMMENT ON COLUMN "student"."schoolclass_id" IS '班级';
CREATE TABLE IF NOT EXISTS "teacher" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "title" VARCHAR(32) NOT NULL,
    "tno" INT NOT NULL
);
COMMENT ON COLUMN "teacher"."name" IS '姓名';
COMMENT ON COLUMN "teacher"."title" IS '职称';
COMMENT ON COLUMN "teacher"."tno" IS '工号';
CREATE TABLE IF NOT EXISTS "course" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "credit" INT NOT NULL,
    "cno" INT NOT NULL,
    "teacher_id" INT NOT NULL REFERENCES "teacher" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "course"."name" IS '课程名称';
COMMENT ON COLUMN "course"."credit" IS '学分';
COMMENT ON COLUMN "course"."cno" IS '课程编号';
COMMENT ON COLUMN "course"."teacher_id" IS '教师';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "student_course" (
    "student_id" INT NOT NULL REFERENCES "student" ("id") ON DELETE CASCADE,
    "course_id" INT NOT NULL REFERENCES "course" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "student_course" IS '课程';
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_student_cou_student_0d222b" ON "student_course" ("student_id", "course_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
