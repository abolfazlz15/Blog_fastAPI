from typing import Any
from pydantic import BaseModel, validator


class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = False


class UserCreate(UserBase):
    password: str

    @validator('username')
    def validate_username(cls: Any, username: str, **kwargs: Any) -> Any:
        if len(username) <= 4:
            raise ValueError('Username cant be empty')
        return username

    @validator('email')
    def validate_email(cls: Any, email: str, **kwargs: Any) -> Any:
        if len(email) == 0:
            raise ValueError('An email is required')
        return email




class Token(BaseModel):
    access_token: str
    token_type: str
