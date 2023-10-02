from beanie import Document, PydanticObjectId
from datetime import datetime, date


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
    category: PydanticObjectId
    viewers: list[str]
    related_blogs: list[PydanticObjectId]
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    publish_at: date | None

    class Settings:
        name = "blogs"
