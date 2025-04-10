from fastapi import APIRouter, HTTPException, Query
from typing import Optional


from models.item import Item
from data.items_data import items


router = APIRouter(prefix="/api/items", tags=["Items"])


@router.post(
        "/items",
        tags=["Items"],
        summary="Create a new item",
        description="Creates a new item and adds it to the inventory.",
        )
def create_item(new_item: Item):
    items.append({
        "id": len(items) + 1,
        "name": new_item.name,
        "price": new_item.price,
    })
    raise HTTPException(status_code=201, detail="Item created successfully")


@router.get(
        "/items",
        tags=["Items"],
        summary="Get all items",
        description="Returns a list of all items in the inventory.",
        )
def get_items():
    return items


@router.get("/items/filter", tags=["Items"], summary="Filter items")
def filter_items(
    min_price: Optional[float] = Query(
        None, ge=0,
        description="Minimum price"),
    max_price: Optional[float] = Query(
        None, le=10000,
        description="Maximum price"),
):
    filtered_items = items
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item["price"] >= min_price]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item["price"] <= max_price]
    return filtered_items


@router.get(
        "/items/{item_id}",
        tags=["Items"],
        summary="Get item by ID",
        description="Returns a single item by its ID.",
        )
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.put(
        "/items/{item_id}",
        tags=["Items"],
        summary="Update an item",
        description="Updates an existing item in the inventory.",
        )
def update_item(item_id: int, updated_item: Item):
    for item in items:
        if item["id"] == item_id:
            item["name"] = updated_item.name
            item["price"] = updated_item.price
            return {"message": "Item updated successfully", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete(
        "/items/{item_id}",
        tags=["Items"],
        summary="Delete an item",
        description="Deletes an item from the inventory.",
        )
def delete_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
