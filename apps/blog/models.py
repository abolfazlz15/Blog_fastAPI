from datetime import datetime
from typing import List

from beanie import Document, Link, PydanticObjectId
from bson import ObjectId
from fastapi import FastAPI, File, UploadFile
from pydantic import Field


class CategorySchema(Document):
    """
    Schema for Category
    """

    title: str
    slug: str

    class Settings:
        name = "categories"


class BlogSchema(Document):
    """
    Schema for Blog
    """

    title: str = Field(max_length=150)
    slug: str = Field(max_length=150)
    author: PydanticObjectId
    cover_image: UploadFile = File()
    content: str
    category: Link[CategorySchema]
    viewers: list[str]
    related_blogs: list[PydanticObjectId]
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    publish_at: datetime | None

    class Settings:
        name = "blogs"

    class Config:
        schema_extra = {
            "example": {
                "title": "How to Create Blog usng FastAPI?",
                "slug": "how-to-create-blog-usng-fastapi",
                "cover_image": "Image File",
                "content": "<h1>Hello</h1>",
                "category": "ObjectId",
                "related_blogs": ["", ""],
                "publish_at": datetime.now(),
            }
        }
