from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) 
    description = Column(String)
    status = Column(String)

    user_id = Column(
    Integer,
    ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="tasks"
    )
