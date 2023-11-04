from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str
