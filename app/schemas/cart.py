from decimal import Decimal
from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, default=1)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]
    total: Decimal