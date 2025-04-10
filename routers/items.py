from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional


router = APIRouter()


items = [
    {
        "id": 1,
        "name": "Asus Tuf Dash F15",
        "price": 4200.0,
    },
    {
        "id": 2,
        "name": "Macbook Pro 16",
        "price": 10000.0,
    },
    {
        "id": 3,
        "name": "Lenovo Legion 5",
        "price": 3500.0,
    },
    {
        "id": 4,
        "name": "Dell XPS 13",
        "price": 5000.0,
    },
    {
        "id": 5,
        "name": "HP Spectre x360",
        "price": 6000.0,
    },
    {
        "id": 6,
        "name": "Acer Swift 3",
        "price": 3000.0,
    },
    {
        "id": 7,
        "name": "Razer Blade Stealth",
        "price": 8000.0,
    },
    {
        "id": 8,
        "name": "Microsoft Surface Laptop 4",
        "price": 7000.0,
    },
    {
        "id": 9,
        "name": "Samsung Galaxy Book Pro",
        "price": 4000.0,
    },
    {
        "id": 10,
        "name": "LG Gram 17",
        "price": 9000.0,
    },
]


class Item(BaseModel):
    name: str = Field(
        min_length=1,  # Minimum length of 1 character
        max_length=100,  # Maximum length of 100 characters
        description="Name of the item must be between 1 and 100 characters"
    )
    price: float = Field(
        ge=0,  # Greater than or equal to 0
        le=10000,  # Less than or equal to 10000
        description="Price of the item must be a positive number"
    )


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
