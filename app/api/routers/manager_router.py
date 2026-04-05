from app.api.deps import get_db, get_current_user, manager_required

from app.schemas.user.UserRegister import UserRegister
from app.schemas.user.UserLogin import UserLogin
from app.schemas.task.TaskCreate import TaskCreate
 
from app.services.user_service import register_user_service, login_user_service, read_account_info_service
from app.services.task_service import read_all_tasks_service, create_task_service

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

manager_router = APIRouter(
    prefix="/manager",
    tags=["manager"],
    responses={404: {"description" : "Not found"}}
)

@manager_router.post("/task/create")
async def create_task(task: TaskCreate, db: Session = Depends(get_db), user = Depends(manager_required)):
    return create_task_service(task, db, user)

@manager_router.delete("/task/delete")
async def delete_task():
    pass