from sqlalchemy.orm import Session

from fastapi import HTTPException, status, Depends

from app.models.task import Task
from app.models.user import User

from app.schemas.task import TaskOut, TaskCreate

from app.api.deps import get_current_user, get_db

def read_all_tasks_service(db: Session = Depends(get_db), user = Depends(get_current_user)):
    user_tasks = db.query(Task).filter(Task.owner_id == user.id).all()
    
    user_task_list = []
    
    for user_task in user_tasks:
        task_out = TaskOut.model_validate(user_task)
        user_task_list.append(task_out)
        
    return user_task_list