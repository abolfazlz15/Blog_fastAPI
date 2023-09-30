from pydantic import BaseModel
from decouple import config
# Database Config
DATABASE_URL = "mongodb://localhost"
DATABASE_PORT = 27017
DATABASE_NAME = "accounting"

# JWT Config
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
ACCSES_TOKEN_LIFETIME = 3600  # seconds
REFRESH_TOKEN_LIFETIME = 86400 * 365  # seconds


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
