from datetime import datetime

from beanie import Document, Link, PydanticObjectId
from typing import List


class CategorySchema(Document):
    """
    Schema for Category
    """

    title: str

    class Settings:
        name = "categories"


class BlogSchema(Document):
    """
    Schema for Blog
    """

    title: str
    author: PydanticObjectId
    cover_image: str | None
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
