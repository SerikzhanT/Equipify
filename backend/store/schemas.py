from typing import List, Optional

from ninja import Schema
from uuid import UUID


class CategorySchema(Schema):
    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryDetailSchema(CategorySchema):
    subcategories: List['CategoryDetailSchema'] = []


class ItemSchema(Schema):
    id: UUID
    name: str
    description: Optional[str] = None
    slug: str
    category_id: int


class ItemDetailSchema(ItemSchema):
    category: CategorySchema


CategoryDetailSchema.model_rebuild()
