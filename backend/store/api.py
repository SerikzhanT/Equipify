from typing import List
from uuid import UUID

from ninja import NinjaAPI
from store.models import Category, Item
from store.schemas import CategoryDetailSchema, CategorySchema, ItemDetailSchema, ItemSchema
from django.shortcuts import get_object_or_404


api = NinjaAPI()


# Категории
@api.get("/categories/", response=List[CategoryDetailSchema])
def list_categories(request):
    categories = Category.objects.filter(parent__isnull=True)
    return [build_category_detail_schema(cat) for cat in categories]


@api.get("/categories/{category_id}/", response=CategoryDetailSchema)
def get_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    return build_category_detail_schema(category)


@api.post("/categories/", response=CategorySchema)
def create_category(request, data: CategorySchema):
    category = Category.objects.create(**data.dict())
    return category


@api.put("/categories/{category_id}/", response=CategorySchema)
def update_category(request, category_id: int, data: CategorySchema):
    category = get_object_or_404(Category, id=category_id)
    for attr, value in data.dict().items():
        setattr(category, attr, value)
    category.save()
    return category


@api.delete("/categories/{category_id}/")
def delete_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return {"success": True}


def build_category_detail_schema(category):
    subcategories = category.get_subcategories()
    return CategoryDetailSchema(
        id=category.id,
        name=category.name,
        description=category.description,
        parent_id=category.parent_id,
        subcategories=[build_category_detail_schema(subcat) for subcat in subcategories]
    )


# Товары
@api.get("/items/", response=List[ItemDetailSchema])
def list_items(request):
    items = Item.objects.all()
    return [build_item_detail_schema(item) for item in items]


@api.get("/items/{slug}/", response=ItemDetailSchema)
def get_item(request, slug: str):
    item = get_object_or_404(Item, slug=slug)
    return build_item_detail_schema(item)


@api.post("/items/", response=ItemSchema)
def create_item(request, data: ItemSchema):
    item = Item.objects.create(**data.dict())
    return item


@api.put("/items/{item_id}/", response=ItemSchema)
def update_item(request, item_id: UUID, data: ItemSchema):
    item = get_object_or_404(Item, id=item_id)
    for attr, value in data.dict().items():
        setattr(item, attr, value)
    item.save()
    return item


@api.delete("/items/{item_id}/")
def delete_item(request, item_id: UUID):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return {"success": True}


def build_item_detail_schema(item):
    return ItemDetailSchema(
        id=item.id,
        name=item.name,
        description=item.description,
        slug=item.slug,
        category_id=item.category.id,
        category=CategorySchema(
            id=item.category.id,
            name=item.category.name,
            description=item.category.description,
            parent_id=item.category.parent_id
        )
    )
