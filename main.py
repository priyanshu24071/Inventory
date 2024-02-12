# app/main.py
from fastapi import FastAPI, HTTPException
from typing import List
from app.models import Item

app = FastAPI()


items_db = []

# Create operation
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items_db.append(item)
    return item

# Read operation (get all items)
@app.get("/items/", response_model=List[Item])
async def read_items():
    return items_db

# Read operation (get single item by ID)
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

# Update operation
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item

# Delete operation
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return deleted_item
