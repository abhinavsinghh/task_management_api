from pydantic import BaseModel
from pydantic import EmailStr

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    user: EmailStr
    username: str


    class Config:
        from_attribute = True
        