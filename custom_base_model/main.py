from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    """Data model for an item on a shopping list."""
    name: str
    description: str | None = None
    price: float
    quantity: int = 1

items = []

@app.post("/items", response_model=list[Item])
def create_item(item: Item):
    """Create a new item and add it to the items list."""
    items.append(item)
    return items

@app.get("/items", response_model=list[Item])
def list_items(limit: int | None = None):
    """List all items in the items list."""
    if limit is not None:
        return items[0:limit]
    return items

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """Get a specific item from the items list."""
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return items[item_id]