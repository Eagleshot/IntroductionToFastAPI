from fastapi import FastAPI, HTTPException

app = FastAPI()

items = []

@app.get("/")
def root():
    return {"message": "Hello, World! :)"}

@app.post("/items")
def create_item(item: str) -> list[str]:
    """Create a new item and add it to the items list."""
    items.append(item)
    return items

@app.get("/items")
def list_items(limit: int | None = None) -> list[str]:
    """List all items in the items list. Optionally limit the number of items returned."""
    if limit is not None:
        return items[0:limit]
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int) -> str:
    """Get a specific item from the items list."""
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail=f"Index {item_id} out of range {len(items)}")
    return items[item_id]
