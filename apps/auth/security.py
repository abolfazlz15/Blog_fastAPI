from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from apps.auth.models import UserInDB
from apps.core.settings import ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(username: str, email: str, expire_date: timedelta):
    encode = {'sub': username, 'email': email}
    expire = datetime.utcnow() + expire_date
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user(db, username: str):
    user = db.find_one({'username': username})
    return UserInDB(**user)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
