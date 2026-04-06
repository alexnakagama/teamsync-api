from app.api.deps import get_db, manager_required

from app.schemas.task.TaskCreate import TaskCreate
 
from app.services.task_service import create_task_service, delete_task_service

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.limiter import limiter

manager_router = APIRouter(
    prefix="/manager",
    tags=["manager"],
    responses={404: {"description" : "Not found"}}
)

@manager_router.post("/task/create")
@limiter.limit("5/minute")
async def create_task(request: Request, task: TaskCreate, db: Session = Depends(get_db), user = Depends(manager_required)):
    return create_task_service(task, db, user)

@manager_router.delete("/task/delete/{task_id}")
@limiter.limit("5/minute")
async def delete_task(request: Request, task_id: int, db: Session = Depends(get_db), user = Depends(manager_required)):
    return delete_task_service(task_id, db, user)