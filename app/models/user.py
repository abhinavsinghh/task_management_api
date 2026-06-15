from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String, unique = True)
    username = Column(String)
    password = Column(String)

    tasks = relationship("Task", back_populates="owner")
    phone_number = Column(String, nullable=True)
    