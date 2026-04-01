from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, index=True, unique=True)
    hashed_pw = Column(String)
    
    tasks = relationship(
        "Task", 
        back_populates="owner",
        # if a user is deleted all his tasks are deleted as well
        cascade="all, delete-orphan"
    )