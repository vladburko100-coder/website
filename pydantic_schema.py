from pydantic import BaseModel
from typing import List


class CartUpdateRequest(BaseModel):
    product_id: int
    quantity: int
    action: str


class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float


class OrderRequest(BaseModel):
    username: str
    items: List[OrderItem]
    total_items: int
    total_price: float
