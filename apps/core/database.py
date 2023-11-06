
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis
from .settings import DATABASE_URL, REDIS_DB, REDIS_DB_HOST, REDIS_DB_PORT

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# redis config
redis_client = redis.Redis(host=REDIS_DB_HOST, port=int(REDIS_DB_PORT), db=int(REDIS_DB))
