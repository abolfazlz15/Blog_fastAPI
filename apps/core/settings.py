from pydantic import BaseModel

# Database Config
DATABASE_URL = "mongodb://localhost"
DATABASE_PORT = 27017
DATABASE_NAME = "accounting"

# JWT Config
SECRET_KEY = "put your secret key here"
ALGORITHM = "HS256"
ACCSES_TOKEN_LIFETIME = 3600  # seconds
REFRESH_TOKEN_LIFETIME = 86400 * 365  # seconds


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
