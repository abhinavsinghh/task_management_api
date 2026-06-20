from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

#DATABASE_URL = 'postgresql://postgres:yourpassword@localhost/taskdb'

engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = sessionlocal()

    try:
        yield db

    finally:
        db.close()

Base = declarative_base()