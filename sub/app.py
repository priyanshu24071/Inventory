from fastapi import FastAPI, HTTPException, Field
from pydantic import BaseModel, Field as PydanticField
from dapr.ext.fastapi import DaprApp

app = FastAPI()
dapr_app = DaprApp(app)


class Item(BaseModel):
    item_no: int = PydanticField(..., title="Item Number", ge=1)
    name: str = PydanticField(..., title="Item Name")
    price: float = PydanticField(..., title="Item Price", gt=0)
    description: str = PydanticField(..., title="Item Description")


# Create an item
@dapr_app.subscribe(pubsub='crudpubsub', topic='create')
@app.post("/items/")
async def create_item(item: Item):
    state_store = dapr_app.get_state_store()
    item_id = str(item.item_no)  # Assuming item_no is unique
    await state_store.save_state(state_store_name="items", key=item_id, value=item.dict())
    return {"message": "Item created successfully"}


# Read all items
@app.get("/items/")
async def read_items():
    state_store = dapr_app.get_state_store()
    items = await state_store.get_state(state_store_name="items")
    if items:
        return items
    else:
        raise HTTPException(status_code=404, detail="No items found")


# Read an item by ID using binary search
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    state_store = dapr_app.get_state_store()
    items = await state_store.get_state(state_store_name="items")
    if items:
        items_ids = list(items.keys())
        low, high = 0, len(items_ids) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_item_id = items_ids[mid]
            if mid_item_id == item_id:
                return items[item_id]
            elif mid_item_id < item_id:
                low = mid + 1
            else:
                high = mid - 1
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        raise HTTPException(status_code=404, detail="No items found")


# Update an item by ID
@dapr_app.subscribe(pubsub='crudpubsub', topic='update')
@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    state_store = dapr_app.get_state_store()
    existing_item_data = await state_store.get_state(state_store_name="items", key=item_id)
    if existing_item_data:
        await state_store.save_state(state_store_name="items", key=item_id, value=item.dict())
        return {"message": "Item updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


# Delete an item by ID
@dapr_app.subscribe(pubsub='crudpubsub', topic='delete')
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    state_store = dapr_app.get_state_store()
    existing_item_data = await state_store.get_state(state_store_name="items", key=item_id)
    if existing_item_data:
        await state_store.delete_state(state_store_name="items", key=item_id)
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
