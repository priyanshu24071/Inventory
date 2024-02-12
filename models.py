from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float = 0.0
