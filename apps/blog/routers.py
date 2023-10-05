import datetime

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

from apps.core.db import db

from .db import create_blog, create_category
from .models import BlogSchema, CategorySchema

router = APIRouter()


@router.post("/")
async def create_new_blog(
    body: BlogSchema = Body(...),
    # Authorize: AuthJWT = Depends(),
):
    body.created_at = datetime.datetime.now()
    # Authorize.jwt_required()
    # current_user = Authorize.get_jwt_subject()
    # body.author = current_user
    new_blog = await create_blog(body)
    return new_blog
