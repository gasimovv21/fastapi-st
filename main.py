from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel


app = FastAPI()

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
    name: str
    price: float


@app.get(
        "/items",
        tags=["Items"],
        summary="Get all items",
        description="Returns a list of all items in the inventory.",
        )
def get_items():
    return items


@app.get(
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


@app.post(
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
    return {"message": "Item created successfully", "item": new_item}


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)  # port, #host, debug=True
