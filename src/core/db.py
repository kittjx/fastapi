import os
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from app.schemas import initialize_pydantic_schemas

DB_URL = os.environ.get("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL is not set")


TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db(app: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    register_tortoise(
        app=app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )
    await Tortoise.generate_schemas()
    initialize_pydantic_schemas()



async def close_db():
    await Tortoise.close_connections()

