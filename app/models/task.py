from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from app.database import Base
from sqlalchemy.orm import relationship

import enum
class PriorityEnum(str, enum.Enum):
    LOW= "LOW"
    MEDIUM= "MEDIUM"
    HIGH= "HIGH"


class StatusEnum(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) 
    description = Column(String)
    status = Column(String)
    priority = Column(Enum(PriorityEnum), default = PriorityEnum.MEDIUM)
    due_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

