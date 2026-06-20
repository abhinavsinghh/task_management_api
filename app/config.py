import os
from dotenv import load_dotenv

from app.database import DATABASE_URL
from app.utils.auth import ACCESS_TOKEN_EXPIRE_MINUTE, SECRET_KEY

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        30
    )
)