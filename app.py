from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.core.db import initiate_database
from apps.auth import routers as AuthRoutes
from apps.blog import routers as BlogRoutes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome"}


app.include_router(AuthRoutes.router, tags=["Authentication"], prefix="/api/v1/auth")
app.include_router(BlogRoutes.router, tags=["Blog"], prefix="/api/v1/blog")
