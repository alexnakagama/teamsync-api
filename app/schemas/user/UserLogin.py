from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    username: str
    email: EmailStr
    password: str