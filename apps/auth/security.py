from datetime import datetime, timedelta
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from apps.core.settings import ALGORITHM, RESET_PASS_ACCSES_TOKEN_LIFETIME, SECRET_KEY
from apps.auth import models, schemas

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def create_access_token(username: str, email: str, expire_date: timedelta):
    encode = {'sub': username, 'email': email}
    expire = datetime.utcnow() + expire_date
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('email')
        return email
    except:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'this token is expire or invalid')


def get_user_by_username(db: Session, username: str) -> Any:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Any:
    return db.query(models.User).filter(models.User.email == email).first()


def get_hash_password(password: str) -> Any:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str) -> Any:
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        email: str = payload.get('email')
        if username is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
        return {'username': username, 'email': email}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hash_password(user['password'])
    del user['password']
    del user['otp']
    user['hashed_password'] = hashed_password
    user_post = models.User(**user)
    db.add(user_post)
    db.commit()
    db.refresh(user_post)
    return user_post


def create_reset_password_token(user: schemas.UserBase, request: Request):
    token_expire_time = timedelta(minutes=RESET_PASS_ACCSES_TOKEN_LIFETIME)
    token = create_access_token(user.username, user.email, token_expire_time)
    token_url = f'{request.base_url}auth/reset-password?token={token}'
    return token_url


def reset_password(user_email: str, user_password: schemas.ResetPasswordIn, db: Session):
    try:
        user = get_user_by_email(db, user_email)
        user.hashed_password = get_hash_password(user_password.new_password)
        db.commit()
    except Exception:
        return False
    return True

def change_user_password(user: str, password: schemas.ChangePasswordIn, db: Session):
    try:
        user = get_user_by_email(db, user)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'invalid email')
        user.hashed_password = get_hash_password(password.new_password)
        db.commit()
        return True
    except Exception:
        return False