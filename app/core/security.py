from datetime import datetime, timedelta, timezone

import jwt

from passlib.context import CryptContext

from app.core.config import settings

from sqlalchemy.orm import Session

from app.models.user import User

from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username was incorrect"
        )
    if not verify_password(password, user.hashed_pw):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password was incorrect"
        )
    return user