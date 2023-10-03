from .models import BlogSchema, CategorySchema

blog_collection = BlogSchema
category_collection = CategorySchema


async def create_blog(new_blog: BlogSchema) -> BlogSchema:
    blog = await new_blog.create()
    return blog


async def create_category(new_category: CategorySchema) -> CategorySchema:
    category = await new_category.create()
    return category
