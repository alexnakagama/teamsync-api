from sqlalchemy.orm import Session

from fastapi import HTTPException, status, Depends

from app.models.task import Task
from app.models.user import User

from app.schemas.task.TaskOut import TaskOut
from app.schemas.task.TaskCreate import TaskCreate

from app.api.deps import get_current_user, get_db

def read_all_tasks_service(db: Session = Depends(get_db), user = Depends(get_current_user)):
    user_tasks = db.query(Task).filter(Task.owner_id == user.id).all()
    
    user_task_list = []
    
    for user_task in user_tasks:
        task_out = TaskOut.model_validate(user_task)
        user_task_list.append(task_out)
        
    return user_task_list

def create_task_service(task_data: TaskCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    assigned_user = db.query(User).filter(User.id == task_data.assigned_user_id).first()
    if not assigned_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User wasnt found or it doesnt exists"
        )
    
    new_task = Task(
        title = task_data.title,
        description = task_data.description,
        owner_id = task_data.assigned_user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskOut.model_validate(new_task)
        