from typing import Any
from pydantic import BaseModel, field_validator, EmailStr, ConfigDict, model_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator('username')
    @classmethod
    def validate_username(cls: Any, username: str, **kwargs: Any) -> Any:
        if len(username) <= 4:
            raise ValueError('Username cant be empty')
        return username

    @field_validator('email')
    @classmethod
    def validate_email(cls: Any, email: EmailStr, **kwargs: Any) -> Any:
        if len(email) == 0:
            raise ValueError('An email is required')
        return email


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class OTPCode(BaseModel):
    otp_code: str


class ResetPasswordIn(BaseModel):
    new_password: str
    new_password_confirm: str

    @model_validator(mode='after')
    def validate_password(self):
        new_password = self.new_password
        new_password_confirm = self.new_password_confirm
        if new_password is not None and new_password_confirm is not None and new_password != new_password_confirm:
            raise ValueError('passwords do not match')
        return self


class ChangePasswordIn(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str

    @model_validator(mode='after')
    def validate_password(self):
        current_password = self.current_password
        new_password = self.new_password
        new_password_confirm = self.new_password_confirm
        if new_password is not None and new_password_confirm is not None and new_password != new_password_confirm:
            if current_password == new_password:
                raise ValueError('your new password cant be like your current password')
            raise ValueError('passwords do not match')
        return self
    

class UserEmail(BaseModel):
    email: str
