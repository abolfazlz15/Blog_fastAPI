import datetime
from typing import List

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
) -> dict:
    # Authorize.jwt_required()
    # current_user = Authorize.get_jwt_subject()
    # body.author = current_user
    body.created_at = datetime.datetime.now()
    new_blog = await create_blog(body)
    return new_blog


@router.get("/")
async def get_all_blogs(
    # Authorize: AuthJWT = Depends(),
) -> List[BlogSchema]:
    # Authorize.jwt_required()
    # current_user = Authorize.get_jwt_subject()
    all_blogs = await BlogSchema.find_all().to_list()
    return all_blogs


@router.get("/{id}/")
async def get_blog_detail(
    id: PydanticObjectId,
    # Authorize: AuthJWT = Depends(),
) -> BlogSchema:
    # Authorize.jwt_required()
    # current_user = Authorize.get_jwt_subject()
    blog = await BlogSchema.get(id)
    return blog
