from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.deps import get_db

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description" : "Not found"}}
)

@users_router.post("register")
async def register_user(db : Session = Depends(get_db)):
    pass

@users_router.post("login")
async def login_user(db: Session = Depends(get_db)):
    pass

@users_router.get("")
async def read_tasks(db: Session = Depends(get_db)):
    pass