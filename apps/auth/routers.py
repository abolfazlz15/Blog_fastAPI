from datetime import timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from apps.auth.email_service import EmailService
from apps.auth.otp_generator import OTPHandler
import json

from apps.auth.security import (
    authenticate_user,
    change_user_password,
    create_access_token,
    create_user,
    get_current_user,
    get_user_by_email,
    get_user_by_username,
    create_reset_password_token, decode_access_token, reset_password,
)
from apps.core.settings import ACCSES_TOKEN_LIFETIME
from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
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
def Login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Incorrect username or password')

    access_token_expires = timedelta(seconds=ACCSES_TOKEN_LIFETIME)
    access_token = create_access_token(
        user.username, user.email, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/regiser/', status_code=status.HTTP_200_OK)
def genrate_otp(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_username = get_user_by_username(db, username=user_data.username)
    db_email = get_user_by_email(db, email=user_data.email)
    if db_username:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Username already registered')
    elif db_email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Email already registered')

    otp = otp_handler.send(user_data.email)
    user_data_dict = user_data.dict()
    user_data_dict['otp'] = otp
    user_data_json = json.dumps(user_data_dict)
    redis_client.setex(otp, 120, user_data_json)
    return {'message': 'OTP code sent'}


@router.post(
    '/verify-otp/',
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def verify_otp(otp_code_data: schemas.OTPCode, db: Session = Depends(get_db)):
    otp_code = otp_code_data.otp_code
    user_data_bytes = redis_client.get(str(otp_code))

    if not user_data_bytes:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Code invalid or expire')

    user_data_json = user_data_bytes.decode('utf-8')
    user_data_dict = json.loads(user_data_json)
    user = create_user(db, user_data_dict)
    return user


@router.post('/forgot-password/', status_code=status.HTTP_200_OK)
def user_forgot_password(request: Request, user_email: schemas.UserEmail , db: Session = Depends(get_db)):
    """sending a email to client for reset password"""

    try:
        user = get_user_by_email(db, user_email.email)
        if user:
            token = create_reset_password_token(user, request)
            email_service.send_reset_password_email(user.email, token)
            return {'message': 'reset password link email sent'}
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'Incorrect Email!')

    except:
        print('user1324')
        HTTPException(status.HTTP_409_CONFLICT, 'something wrong')


@router.post('/reset-password/', status_code=status.HTTP_200_OK)
def user_reset_password(user_password: schemas.ResetPasswordIn, token: str, db: Session = Depends(get_db)):
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'your link expired or wrong')
    reset_pass = reset_password(email, user_password, db)
    if not reset_pass:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'something wrong')
    return {'message': 'Your password has been successfully changed'}


@router.post('/change-passowrd/', status_code=status.HTTP_200_OK)
def user_change_password(
    current_user: Annotated[schemas.UserBase, Depends(get_current_user)],
    user_new_password: schemas.ChangePasswordIn,
    db: Session = Depends(get_db)
    ):
    new_password = change_user_password(current_user, user_new_password, db)

    if not new_password:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'something wrong')
    return {'message': 'Your password has been successfully changed'}