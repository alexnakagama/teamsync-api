from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    is_completed = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship(
        "User", 
        back_populates="tasks"
    )
    