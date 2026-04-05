from pydantic import BaseModel

class TaskCreate(BaseModel):
    title : str
    description: str
    is_completed : bool = False
    assigned_user_id: int