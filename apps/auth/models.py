from beanie import Document
from pydantic import BaseModel, Field

from apps.auth.utils.validation import ObjectIdStr


class User(BaseModel):
    username: str
    email: str
    is_active: bool | None = None
    is_admin: bool = False


class UserInDB(User):
    hashed_password: str


class UserAccsesSchema(Document):
    """
    Schema for User Accses
    """

    accses_name: str | None = Field(title="User Accses Name")
    institute: str | None = Field(title="User Accses Name")
    permissions: dict | None = Field(title="User Accses Permissions")
    username: str | None = Field(title="User Accses Username")
    password: str | None = Field(title="User Accses Password", min_length=8)

    class Settings:
        name = "user_accsess"



class LoginSchema(BaseModel):
    """
    Login Schema for User
    """

    username: str
    password: Field(min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "12345678",
            }
        }


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    id: ObjectIdStr
    email: str
