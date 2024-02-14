from typing import List, Optional
import os
from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
import redis

app = FastAPI()

app_port = os.getenv('APP_PORT', '6001')

class Item(BaseModel):
    item_id: int
    name: str
    price: float
    description: str
    tax: float

class Database:
    def _init_(self):
        self.redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.item_id_counter = 1

    def add_item(self, item: Item):
        item.item_id = self.item_id_counter
        self.item_id_counter += 1
        self.redis_conn.hmset(f'item:{item.item_id}', item.dict())

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        item_data = self.redis_conn.hgetall(f'item:{item_id}')
        if not item_data:
            return None
        return Item(**item_data)

    def update_item(self, item_id: int, item: Item):
        self.redis_conn.hmset(f'item:{item_id}', item.dict())

    def delete_item(self, item_id: int):
        self.redis_conn.delete(f'item:{item_id}')

db = Database()  # Initialize database

@app.websocket('/crud_subscriptions')
async def subscribe_crud_subscriptions(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.receive_text()

@app.post('/items/', response_model=Item)
async def create_item(item: Item):
    db.add_item(item)
    return item

@app.get('/items/{item_id}', response_model=Item)
async def read_item(item_id: int):
    item = db.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put('/items/{item_id}', response_model=Item)
async def update_item(item_id: int, item: Item):
    db.update_item(item_id, item)
    return item

@app.delete('/items/{item_id}')
async def delete_item(item_id: int):
    db.delete_item(item_id)
    return {"message": "Item deleted successfully"}
