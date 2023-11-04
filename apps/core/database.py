
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import DATABASE_URL

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


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastAPI_blog_db', user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database Connection was OK')
#         break
#     except Exception as e:
#         print('Database Connection Faild')
#         print(e)
#         time.sleep(10)