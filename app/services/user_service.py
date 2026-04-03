from app.models.user import User

from app.schemas.user.UserRegister import UserRegister
from app.schemas.user.UserLogin import UserLogin
from app.schemas.user.UserOut import UserOut

from app.core.security import get_password_hash, authenticate_user, create_access_token

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
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
        hashed_pw = hashed_password,
        # role will be assignated automatically with: "user"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserOut.model_validate(new_user)

def login_user_service(db: Session, form_data: OAuth2PasswordRequestForm) -> dict:
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut.model_validate(user)
    }

