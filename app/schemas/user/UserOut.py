from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    id : int
    email: EmailStr
    username: str
    
    model_config = {"from_attributes" : True}