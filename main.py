from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from redis import Redis
from dapr.ext.fastapi import Dapr
from dapr.clients import DaprClient

app = FastAPI()
dapr = Dapr()

# Connect to Redis
redis = Redis(host='localhost', port=6379, db=0)

# Define Item model
class Item(BaseModel):
    name: str
    description: str
    price: float

# CRUD operations
@app.post("/items/", response_model=Item)
async def create_item(item: Item, dapr_client: DaprClient = Depends(dapr.dapr_client)):
    # Add item to Redis
    item_id = redis.incr('item_id_counter')
    redis_key = f'item:{item_id}'
    redis.hmset(redis_key, item.dict())

    # Publish 'item_created' event
    await dapr_client.publish_event("pubsub", "item_created", data={"item_id": item_id})

    return item

@app.get("/items/", response_model=list[Item])
async def read_items():
    # Retrieve all items from Redis
    keys = redis.keys('item:*')
    items = [redis.hgetall(key) for key in keys]
    return items

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    # Retrieve item from Redis
    redis_key = f'item:{item_id}'
    item = redis.hgetall(redis_key)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item, dapr_client: DaprClient = Depends(dapr.dapr_client)):
    # Update item in Redis
    redis_key = f'item:{item_id}'
    if not redis.exists(redis_key):
        raise HTTPException(status_code=404, detail="Item not found")
    redis.hmset(redis_key, item.dict())

    # Publish 'item_updated' event
    await dapr_client.publish_event("pubsub", "item_updated", data={"item_id": item_id})

    return item

@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int, dapr_client: DaprClient = Depends(dapr.dapr_client)):
    # Delete item from Redis
    redis_key = f'item:{item_id}'
    if not redis.exists(redis_key):
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = redis.hgetall(redis_key)
    redis.delete(redis_key)

    # Publish 'item_deleted' event
    await dapr_client.publish_event("pubsub", "item_deleted", data={"item_id": item_id})

    return deleted_item

# Pub/Sub event handlers
@app.post("/pubsub/item_created")
async def handle_item_created(event: dict):
    print(f"Item created: {event}")

@app.post("/pubsub/item_updated")
async def handle_item_updated(event: dict):
    print(f"Item updated: {event}")

@app.post("/pubsub/item_deleted")
async def handle_item_deleted(event: dict):
    print(f"Item deleted: {event}")
