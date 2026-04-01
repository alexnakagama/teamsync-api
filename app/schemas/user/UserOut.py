from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    id : int
    email: EmailStr
    username: str
    
    class Config:
        from_attributes = True 