from apps.auth import schemas
from apps.auth.schemas import UserBase
from apps.auth.models import User
from apps.auth.security import get_hash_password, get_user_by_username


class UserRepository:
    def __init__(self, session):
        self.session = session

    def create_user(self, user: schemas.UserCreate):
        hashed_password = get_hash_password(user['password'])
        del user['password']
        del user['otp']
        user['hashed_password'] = hashed_password
        db_user = User(**user)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, user_email: str):
        return self.session.query(User).filter(User.email == user_email).first()
    
    def get_user_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def update_user(self, username: str, user_data: UserBase):
        db_user = get_user_by_username(self.session, username)
        if db_user:
            for key, value in user_data.items():
                setattr(db_user, key, value)
            self.session.commit()
            self.session.refresh(db_user)
            return db_user
        return None

    def delete_user(self, user_id):
        db_user = self.get_user(user_id)
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
            return db_user
        return None
    