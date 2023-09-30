from datetime import datetime, timedelta
from core.settings import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt


def create_access_token(username: str, user_id: str, expire_date: timedelta):
    encode = {'sub': username, 'id': user_id}
    expire = datetime.utcnow() + expire_date
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

