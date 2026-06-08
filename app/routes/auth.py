from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password

router = APIRouter(tags=["Authentication"])

@router.post('/register')
def register(user:UserCreate, db:Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, username=user.username, password=user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'User Registered'}