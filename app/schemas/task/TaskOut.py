from pydantic import BaseModel

class TaskOut(BaseModel):
    id : int
    title : str
    description : str
    is_completed : bool
    owner_id : int
    
    class Config:
        from_attributes = True