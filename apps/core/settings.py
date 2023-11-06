from decouple import config
from pydantic import BaseModel

# Database Config
DATABASE_HOSTNAME = config('DATABASE_HOSTNAME')
DATABASE_USERNAME = config('DATABASE_USERNAME')
DATABASE_PASSWORD = config('DATABASE_PASSWORD')
DATABASE_NAME = config('DATABASE_NAME')
DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}/{DATABASE_NAME}'

# JWT Config
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = 'HS256'
ACCSES_TOKEN_LIFETIME = 3600  # seconds
REFRESH_TOKEN_LIFETIME = 86400 * 365  # seconds

# Email Config
SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT')
SENDER_EMAIL = config('SENDER_EMAIL')
EMAIL_PASSWORD = config('EMAIL_PASSWORD')

REDIS_DB = config('REDIS_DB')
REDIS_DB_HOST = config('REDIS_DB_HOST')
REDIS_DB_PORT = config('REDIS_DB_PORT')

class Settings(BaseModel):
    authjwt_secret_key: str = 'secret'
