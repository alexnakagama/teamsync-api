from fastapi import FastAPI

from app.api.routers.users_router import users_router
from app.api.routers.manager_router import manager_router

from app.db.database import Base, engine

from app.models.user import User
from app.models.task import Task

app = FastAPI(title="TeamSync API")

Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(manager_router)