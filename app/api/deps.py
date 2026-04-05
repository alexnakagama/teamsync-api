from typing import Generator

from sqlalchemy.orm import Session
from app.db.database import SessionLocal

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

import jwt

from app.core.config import settings

from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def manager_required(user = Depends(get_current_user)):
    if user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a manager, cant create tasks"
        )
    return user