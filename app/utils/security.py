from passlib.context import CryptContext
import bcrypt

print("BCRYPT FILE:", bcrypt.__file__)
print("BCRYPT VERSION:", getattr(bcrypt, "__version__", "NO_VERSION"))
print("HAS ABOUT:", hasattr(bcrypt, "__about__"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)