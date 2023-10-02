from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from apps.auth.models import TokenSchema, UserSchema
from apps.auth.security import (authenticate_user, create_access_token,
                                get_current_user)
from apps.core.db import get_user_collection
from apps.core.settings import ACCSES_TOKEN_LIFETIME

router = APIRouter()


def get_collection():
    return USERS_COLLECTION


@router.post('/login/', response_model=TokenSchema)
async def Login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: UserSchema = Depends(get_user_collection)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password')
    
    access_token_expires = timedelta(seconds=ACCSES_TOKEN_LIFETIME)
    token = create_access_token(user.username, user.email, access_token_expires)

    return {'access_token': token, 'token_type': 'bearer'}


