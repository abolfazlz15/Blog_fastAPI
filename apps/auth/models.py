from sqlalchemy import TIMESTAMP, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql.expression import text

from apps.core.database import Base


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(50), unique=True)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
