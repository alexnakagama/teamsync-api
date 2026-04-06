from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, manager_required

from app.schemas.user.UserRegister import UserRegister
from app.schemas.user.UserLogin import UserLogin
from app.schemas.task.TaskCreate import TaskCreate
 
from app.services.user_service import register_user_service, login_user_service, read_account_info_service
from app.services.task_service import read_all_tasks_service, create_task_service

from app.core.limiter import limiter

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description" : "Not found"}}
)

@users_router.post("/register")
@limiter.limit("5/minute")
async def register_user(request: Request, user: UserRegister ,db: Session = Depends(get_db)):
    return register_user_service(db, user)

@users_router.post("/login")
@limiter.limit("5/minute")
async def login_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_user_service(db, form_data)

@users_router.get("/tasks")
@limiter.limit("5/minute")
async def read_all_tasks(request: Request, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return read_all_tasks_service(db, user)

@users_router.get("/me/{user_id}")
@limiter.limit("5/minute")
async def read_account_info(request: Request, user_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return read_account_info_service(db, user_id)