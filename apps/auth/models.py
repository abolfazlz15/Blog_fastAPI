from beanie import Document
from pydantic import BaseModel, Field

from apps.auth.utils.validation import ObjectIdStr


class UserSchema(Document):
    """
    Schema for User Accses
    """
    id: ObjectIdStr
    email: str
    username: str | None = Field(title="User Accses Username")
    password: str | None = Field(title="User Accses Password", min_length=8)
    is_active: bool | None = None
    is_admin: bool = False

    class Settings:
        name = "user_accsess"


class UserInDB(UserSchema):
    hashed_password: str


class UserCreateRequestSchema(BaseModel):
    """
    Login Schema for User
    """
    email: str
    username: str
    password: str

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
