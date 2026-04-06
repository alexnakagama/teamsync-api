from app.api.deps import get_db, get_current_user, manager_required

from app.schemas.task.TaskCreate import TaskCreate
 
from app.services.task_service import create_task_service, delete_task_service

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

@manager_router.delete("/task/delete/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db), user = Depends(manager_required)):
    return delete_task_service(task_id, db, user)