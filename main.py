from apps.blog import routers as BlogRoutes
from apps.core import database, models
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from apps.auth import routers as AuthRoutes
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get('/', tags=['Root'])
def read_root():
    return {'message': 'This is Root'}


@app.get('/sqlalchemy')
def test_root(db: Session = Depends(database.get_db)):
    return {'status': 'OK'}


app.include_router(BlogRoutes.router, tags=['Blog'])
app.include_router(AuthRoutes.router, tags=['auth'])
