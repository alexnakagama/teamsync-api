from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    email: EmailStr
    username: str
    
    class Config:
        from_attributes = True 