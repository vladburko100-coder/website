from pydantic import BaseModel


class CartUpdateRequest(BaseModel):
    product_id: int
    quantity: int
    action: str