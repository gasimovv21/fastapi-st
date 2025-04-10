import aiofiles
import json


from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.item import Item
from data.items_data import items

from utils.git_versioning import commit_material_change, get_material_changelog


router = APIRouter(prefix="/api/items", tags=["Items"])


DATA_FILE = Path("data/items.json")
DATA_DIR = DATA_FILE.parent


async def save_items():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(DATA_FILE, "w") as f:
        await f.write(json.dumps(items, indent=4))


@router.post(
        "/items",
        tags=["Items"],
        summary="Create a new item",
        description="Creates a new item and adds it to the inventory.",
        )
async def create_item(new_item: Item):
    items.append({
        "id": len(items) + 1,
        "name": new_item.name,
        "price": new_item.price,
    })

    await save_items()
    commit_material_change(
        materials_path=DATA_DIR,
        file_path=DATA_FILE,
        message="Added new item"
    )

    raise HTTPException(status_code=201, detail="Item created successfully")


@router.get(
        "/items",
        tags=["Items"],
        summary="Get all items",
        description="Returns a list of all items in the inventory.",
        )
def get_items():
    return items


@router.post("/items/save", tags=["Items"], summary="Save items to file")
async def save_items_to_file(file_path: str = "items.json"):
    try:
        async with aiofiles.open(file_path, "w") as f:
            content = json.dumps(items, indent=4)
            await f.write(content)
        return {"message": f"Items saved to {file_path}"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving items: {str(e)}")


@router.post("/items/load", tags=["Items"], summary="Load items from file")
async def load_items_from_file(file_path: str = "items.json"):
    try:
        async with aiofiles.open(file_path, "r") as f:
            content = await f.read()
            loaded_items = json.loads(content)
            items.clear()
            items.extend(loaded_items)
        return {"message": f"Items loaded from {file_path}"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading items: {str(e)}")


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


@router.get("/items/changelog", tags=["Items"])
def get_items_changelog():
    return {
        "changelog": get_material_changelog(DATA_DIR, DATA_FILE)
    }


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
async def update_item(item_id: int, updated_item: Item):
    for item in items:
        if item["id"] == item_id:
            item["name"] = updated_item.name
            item["price"] = updated_item.price

            await save_items()
            commit_material_change(
                materials_path=DATA_DIR,
                file_path=DATA_FILE,
                message=f"Updated item: {updated_item.name}",
            )
            return {"message": "Item updated successfully", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete(
        "/items/{item_id}",
        tags=["Items"],
        summary="Delete an item",
        description="Deletes an item from the inventory.",
        )
async def delete_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            items.remove(item)

            await save_items()
            commit_material_change(
                materials_path=DATA_DIR,
                file_path=DATA_FILE,
                message=f"Deleted item: {item['name']}",
            )
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

