from pydantic import BaseModel
from datetime import datetime


class AddToWishlistRequest(BaseModel):
    product_id: int


class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: "Decimal"
    added_at: datetime

    class Config:
        from_attributes = True