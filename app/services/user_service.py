from app.models.user import User

from app.schemas.user.UserRegister import UserRegister
from app.schemas.user.UserLogin import UserLogin
from app.schemas.user.UserOut import UserOut

from app.core.security import get_password_hash, verify_password, create_access_token

from sqlalchemy.orm import Session

from fastapi import HTTPException, status

def register_user_service(db: Session, user_in: UserRegister) -> UserOut:
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user already exists"
        )
    
    hashed_password = get_password_hash(user_in.password)
    
    new_user = User(
        email = user_in.email,
        username = user_in.username,
        hashed_password = hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserOut.model_validate(new_user)

def login_user_service(db: Session, user_in: UserLogin) -> dict:
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesnt exists"
        )
    
    if not verify_password(user_in.password, existing_user.hashed_pw):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password was incorrect"
        )
    
    access_token = create_access_token({"sub": existing_user.id})

    return {
        "access_token": access_token, 
        "token_type": "bearer",       
        "user": UserOut.model_validate(existing_user)  
    }