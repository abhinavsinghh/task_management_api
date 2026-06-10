from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password
from app.utils.auth import create_access_token

router = APIRouter(tags=["Authentication"])

@router.post('/register')
def register(user:UserCreate, db:Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, username=user.username, password=user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'User Registered'}


@router.post('/login')
def login(user:UserLogin, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return {'message':'Invalid Credentials'}
    
    if not verify_password(user.password, db_user.password):
        return {'message':'Invalid Credentials'}

    token = create_access_token({'sub':db_user.email})
    return {'access_token': token, 'token_type': 'bearer'}