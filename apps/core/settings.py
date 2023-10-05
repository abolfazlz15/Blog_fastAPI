from decouple import config
from pydantic import BaseModel

# Database Config
DATABASE_URL = "mongodb://localhost"
DATABASE_PORT = 27017
DATABASE_NAME = "fast_blog"

# JWT Config
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
ACCSES_TOKEN_LIFETIME = 3600  # seconds
REFRESH_TOKEN_LIFETIME = 86400 * 365  # seconds

# Email Config
SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT')
SENDER_EMAIL = config('SENDER_EMAIL')
EMAIL_PASSWORD = config('EMAIL_PASSWORD')

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
