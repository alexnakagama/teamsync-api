from pydantic import BaseModel, EmailStr

class UserDelete(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str