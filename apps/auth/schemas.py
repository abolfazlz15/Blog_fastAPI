from typing import Any
from pydantic import BaseModel, validator


class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = False

