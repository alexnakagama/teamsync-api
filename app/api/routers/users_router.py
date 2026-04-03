from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.models.user import User

from app.api.deps import get_db, get_current_user

from app.schemas.user.UserRegister import UserRegister
from app.schemas.user.UserLogin import UserLogin
 
from app.services.user_service import register_user_service, login_user_service

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description" : "Not found"}}
)

@users_router.post("/register")
async def register_user(user: UserRegister ,db: Session = Depends(get_db)):
    return register_user_service(db, user)

@users_router.post("/login")
async def login_user(user_in: UserLogin ,db: Session = Depends(get_db)):
    return login_user_service(db, user_in)
