import time
from datetime import timedelta
from typing import Annotated
from sqlalchemy.orm import Session

import psycopg2
from apps.auth.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from apps.core.settings import ACCSES_TOKEN_LIFETIME
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from apps.core.database import get_db
from apps.auth import schemas


router = APIRouter()



@router.post('/login/', response_model=schemas.Token)
async def Login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password')
    
    access_token_expires = timedelta(seconds=ACCSES_TOKEN_LIFETIME)
    access_token = create_access_token(user.username, user.email, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}