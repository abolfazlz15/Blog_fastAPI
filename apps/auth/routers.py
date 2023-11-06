from datetime import timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from apps.auth.email_service import EmailService
from apps.auth.otp_generator import OTPHandler
import json

from apps.auth.security import (
    authenticate_user,
    create_access_token,
    get_user_by_email,
    get_user_by_username,
)
from apps.core.settings import ACCSES_TOKEN_LIFETIME
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from apps.core.database import get_db, redis_client
from apps.auth import schemas
from apps.core import settings

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


email_service = EmailService(smtp_server=settings.SMTP_SERVER,
                             smtp_port=int(settings.SMTP_PORT),
                             sender_email=settings.SENDER_EMAIL,
                             sender_password=settings.EMAIL_PASSWORD)

otp_handler = OTPHandler(email_service)


@router.post('/login/', response_model=schemas.Token)
async def Login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password')

    access_token_expires = timedelta(seconds=ACCSES_TOKEN_LIFETIME)
    access_token = create_access_token(
        user.username, user.email, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/regiser/')
async def genrate_otp(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_username = get_user_by_username(db, username=user_data.username)
    db_email = get_user_by_email(db, email=user_data.email)
    if db_username:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    elif db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    otp = otp_handler.send(user_data.email)
    
    user_data_json = json.dumps(user_data.dict())
    redis_client.setex(otp, 120, user_data_json)
    return {'message': 'OTP code sent'}