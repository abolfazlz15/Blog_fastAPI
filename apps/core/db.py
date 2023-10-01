import pydantic
from beanie import init_beanie
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from . import settings

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

client = MongoClient(settings.DATABASE_URL, settings.DATABASE_PORT)
db = client[settings.DATABASE_NAME]

USERS_COLLECTION = db['users']


async def initiate_database():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            # Schema
        ],
    )
