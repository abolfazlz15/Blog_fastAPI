from decouple import config
from pydantic import BaseModel

# Database Config
DATABASE_HOSTNAME = config('DATABASE_HOSTNAME', '127.0.0.1')
DATABASE_USERNAME = config('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = config('DATABASE_PASSWORD', 'pass')
DATABASE_NAME = config('DATABASE_NAME', 'postgres')
DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}/{DATABASE_NAME}'
DATABASE_URL = "postgresql://postgres:pass@localhost/postgres"

# JWT Config
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = 'HS256'
ACCSES_TOKEN_LIFETIME = 3600  # seconds
RESET_PASS_ACCSES_TOKEN_LIFETIME = 10  # minutes
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
