from beanie import Document
from pydantic import BaseModel, Field


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
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "12345678",
            }
        }
