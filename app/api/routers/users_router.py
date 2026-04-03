from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.schemas.user.UserRegister import UserRegister

users_router = APIRouter(
    prefix="users",
    tags=["users"],
    responses={404: {"description" : "Not found"}}
)

@users_router.post("/register")
async def register_user(db: Session = Depends(get_db)):
    pass

@users_router.post("/login")
async def login_user(db: Session = Depends(get_db)):
    pass
